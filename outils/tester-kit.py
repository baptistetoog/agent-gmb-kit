"""Teste le parcours complet du kit, sans serveur : fiche de paramètres -> prompts personnalisés -> document -> liens.

python3 outils/tester-kit.py            (ajouter --sans-reseau pour ne pas tester les liens)

1. chaque variable des prompts est définie dans parametres.md, et chaque paramètre sert ;
2. deux fiches complètes (un établissement / un réseau) donnent 14 prompts sans aucune variable restante ;
3. les blocs de prompt sont bien fermés et le document HTML contient tous les prompts ;
4. la charte et le personnage de la fiche arrivent bien dans les prompts ;
5. les liens publics cités par les prompts répondent (dont la scène 3D sur GitHub).
"""
import re
import shutil
import sys
import tempfile
import subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT))
import personnaliser  # noqa: E402

VARIABLE = re.compile(r"\{[A-Z_0-9]+\}")
erreurs = []


def verifier(condition, message):
    print(("  ✅ " if condition else "  ❌ ") + message)
    if not condition:
        erreurs.append(message)


def fiche(base, valeurs):
    """Copie de parametres.md avec certaines valeurs remplacées."""
    texte = (KIT / "parametres.md").read_text(encoding="utf-8")
    for var, val in valeurs.items():
        texte = re.sub(rf"^\| \{{{var}\}} \| [^|]* \|", f"| {{{var}}} | {val} |", texte, flags=re.M)
    p = base / f"fiche-{valeurs['ENTREPRISE'].lower().replace(' ', '-')}.md"
    p.write_text(texte, encoding="utf-8")
    return p


print("1. Variables")
prompts = sorted((KIT / "prompts").glob("*.md"))
utilisees = set(VARIABLE.findall("".join(p.read_text(encoding="utf-8") for p in prompts)))
definies, _ = personnaliser.lire_parametres(KIT / "parametres.md")
verifier(len(prompts) == 14, f"14 prompts trouvés ({len(prompts)})")
verifier(not (utilisees - set(definies)), f"toutes les variables des prompts sont définies {sorted(utilisees - set(definies)) or ''}")
inutiles = set(definies) - utilisees - {"{DEPOT_BRUT}"}
verifier(not inutiles, f"tous les paramètres servent {sorted(inutiles) or ''}")

COMMUN = dict(DOMAINE="agent.exemple-test.fr", UTILISATEUR="exempletest", EMAIL_ADMIN="admin@exemple-test.fr",
              SITE_WEB="https://www.exemple-test.fr", TON="tutoiement, fun et dynamique",
              NOM_AGENT="Jumpy", COULEUR_AGENT="#1B3A8C", COULEUR_YEUX="#FFD400", BADGE="JUMP", ACCESSOIRE="casque",
              COULEUR_FOND="#F4F7FF", COULEUR_ACCENT="#E6007E", COULEUR_ACCENT_2="#00B5E2", COULEUR_TEXTE="#14161F",
              POLICE_TITRES="Baloo 2", POLICE_TEXTE="Nunito", LOGO="https://www.exemple-test.fr/logo.svg",
              CHARTE_CONSIGNES="style ludique, coins très arrondis")
CAS = {
    "un établissement": dict(COMMUN, ENTREPRISE="Boulangerie Test", ACTIVITE="boulangerie pâtisserie artisanale",
                             ETABLISSEMENTS="un seul établissement", MOMENT_CLIENT="l'achat"),
    "un réseau": dict(COMMUN, ENTREPRISE="Reseau Test", ACTIVITE="parcs de loisirs indoor",
                      ETABLISSEMENTS="tous les parcs du réseau, chacun avec sa propre fiche Google",
                      MOMENT_CLIENT="la visite au parc", SIGNATURE="L'équipe Reseau Test suivie du nom du parc"),
}

tmp = Path(tempfile.mkdtemp())
sorties = {}
try:
    for cas, valeurs in CAS.items():
        print(f"\n2-4. Personnalisation : {cas} ({valeurs['ENTREPRISE']})")
        f = fiche(tmp, valeurs)
        sys.argv = ["personnaliser.py", str(f)]
        personnaliser.main()
        sortie = KIT / "mes-prompts" / valeurs["ENTREPRISE"].lower().replace(" ", "-")
        sorties[cas] = sortie
        fichiers = sorted(sortie.glob("*.md"))
        texte = "".join(p.read_text(encoding="utf-8") for p in fichiers)
        verifier(len(fichiers) == 14, "14 prompts personnalisés")
        verifier(not VARIABLE.findall(texte), f"aucune variable restante {sorted(set(VARIABLE.findall(texte))) or ''}")
        verifier("compléter" not in texte.lower().replace("« à compléter »", "").replace("à compléter » ce", ""),
                 "aucune valeur « À compléter » recopiée")
        verifier(all(p.read_text(encoding="utf-8").count("```") % 2 == 0 for p in fichiers), "tous les blocs de prompt sont fermés")
        p5 = (sortie / "05-agent-visuel.md").read_text(encoding="utf-8")
        verifier(all(valeurs[k] in p5 for k in ("COULEUR_ACCENT", "COULEUR_FOND", "POLICE_TITRES", "NOM_AGENT", "BADGE")),
                 "charte et personnage présents dans le prompt 5")
        p3 = (sortie / "03-outil-connexion.md").read_text(encoding="utf-8")
        verifier(valeurs["ETABLISSEMENTS"] in p3 and valeurs["ACTIVITE"] in p3, "périmètre et activité recopiés dans PROJET.md (prompt 3)")
        docs = list(sortie.glob("*.html"))
        html = docs[0].read_text(encoding="utf-8") if docs else ""
        nb_blocs = texte.count("```") // 2
        verifier(len(docs) == 1 and html.count('class="prompt"') + html.count('class="cmd"') == nb_blocs,
                 f"document HTML complet ({nb_blocs} blocs)")
        verifier(valeurs["COULEUR_ACCENT"] in html, "le document prend la couleur d'accent de la fiche")
finally:
    shutil.rmtree(tmp)
    for s in sorties.values():
        shutil.rmtree(s, ignore_errors=True)

if "--sans-reseau" not in sys.argv:
    print("\n5. Liens publics cités par les prompts")
    textes = "".join(p.read_text(encoding="utf-8") for p in prompts)
    textes = textes.replace("{DEPOT_BRUT}", definies["{DEPOT_BRUT}"]).replace("{DEPOT}", definies["{DEPOT}"])
    liens = sorted({u.rstrip(".,;:»)`'") for u in re.findall(r"https://[^\s<>()\"`]+", textes) if "{" not in u})
    liens = [u for u in liens if not re.search(r"monentreprise|exemple|/oauth/retour|\.well-known", u)]
    for u in liens:
        # curl plutôt que urllib : le Python livré avec macOS refuse certains serveurs TLS récents
        r = subprocess.run(["curl", "-s", "-m", "15", "-o", "/dev/null", "-w", "%{http_code}", "-L", "-A", "tester-kit/1.0", u],
                           capture_output=True, text=True)
        code = int(r.stdout) if r.stdout.isdigit() and r.stdout != "000" else "injoignable"
        # un serveur MCP ou une API peut répondre 401/405 à un simple GET : il existe bien
        ok = code == 200 or (code in (401, 405, 406) and ("mcp" in u or "api." in u))
        verifier(ok, f"{code}  {u}")

print("\n" + ("✅ Parcours du kit OK" if not erreurs else f"❌ {len(erreurs)} problème(s)"))
sys.exit(1 if erreurs else 0)
