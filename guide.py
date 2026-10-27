"""Fabrique LE guide complet d'une entreprise, en un seul fichier HTML à ouvrir dans le navigateur :
connexion SSH au VPS du client, sous-domaine, les 14 étapes avec leurs prompts, puis le résultat final.

python3 guide.py exemples/newjump.md   ->  mes-prompts/<entreprise>/Guide complet - <entreprise>.html

Les valeurs encore « À compléter » (domaine, e-mail…) et l'accès au VPS se tapent en haut de la page :
elles se recopient alors dans tous les prompts, et chaque prompt a son bouton « Copier ».
"""
import html
import re
import sys
from pathlib import Path

import build_doc
import personnaliser

ICI = Path(__file__).parent
E = html.escape

# les champs à remplir dans la page : (variable, libellé, exemple)
CHAMPS = {
    "ALIAS": ("Nom du raccourci SSH", "vps"),
    "IP": ("Adresse IP du VPS du client", "51.210.12.34"),
    "{DOMAINE}": ("Sous-domaine de l'outil", "agent.monentreprise.fr"),
    "{EMAIL_ADMIN}": ("Votre e-mail de connexion à l'outil", "vous@exemple.fr"),
    "{SITE_WEB}": ("Site internet de l'entreprise", "https://www.monentreprise.fr"),
    "{ACTIVITE}": ("Activité en une phrase", "parc de loisirs indoor pour enfants et adultes"),
    "{TON}": ("Ton de l'agent", "tutoiement, fun et dynamique"),
}


VALEUR_ALIAS = ' value="vps"'


def jeton(nom):
    return f"\x00{nom.strip('{}')}\x00"


def exemple(valeur, defaut):
    m = re.search(r"\(ex\. ([^)]+)\)", valeur)
    return m.group(1) if m else defaut


def avant(entreprise, utilisateur):
    """Les étapes faites à la main avant le premier prompt."""
    return f"""
# Étape 0. Ce qu'il faut avant de commencer

**Ce qu'on voit à la fin :** tout est réuni pour installer l'agent d'une traite.

À demander au client :
- l'adresse IP de son VPS (Ubuntu 24.04) et l'accès root : mot de passe root ou clé SSH, envoyés par l'hébergeur (OVH, Hostinger, Scaleway, IONOS…) ;
- un accès à la zone DNS de son nom de domaine, ou une personne qui peut y ajouter une ligne ;
- un accès « propriétaire » ou « gestionnaire » au compte Google qui gère les fiches Google de {entreprise}.

De votre côté :
- Claude Code installé sur votre ordinateur (sinon : `curl -fsSL https://claude.ai/install.sh | bash`) ;
- l'abonnement Claude (Pro ou Max) que l'agent utilisera ;
- un compte Activepieces (https://cloud.activepieces.com).

Remplissez les cases en haut de cette page : elles se recopient dans toutes les commandes et tous les prompts.

# Étape A. Se connecter au VPS du client en SSH

**Ce qu'on voit à la fin :** la commande `ssh {jeton("ALIAS")}` ouvre le serveur du client sans demander de mot de passe. Tous les prompts s'en servent.

Toutes ces commandes se lancent dans le terminal de votre ordinateur.

1. Vérifier que vous avez une clé SSH (si la commande affiche une ligne qui commence par ssh-ed25519, passez au point 2) :

```bash
cat ~/.ssh/id_ed25519.pub
```

Sinon, créez-la (appuyez sur Entrée à chaque question) :

```bash
ssh-keygen -t ed25519 -C "toog-expertise"
```

2. Déposer votre clé sur le VPS. Tapez « yes » à la première question, puis le mot de passe root donné par l'hébergeur (il ne s'affiche pas). C'est la seule fois où il sera demandé. Si l'hébergeur a déjà installé votre clé, sautez ce point.

```bash
ssh-copy-id root@{jeton("IP")}
```

3. Vérifier que le nom du raccourci n'est pas déjà pris. Si `{jeton("ALIAS")}` apparaît dans la liste (par exemple pour le serveur de la démo), changez le « Nom du raccourci SSH » en haut de la page, par exemple vps-{utilisateur} : tous les prompts suivront.

```bash
grep -n "^Host " ~/.ssh/config
```

4. Créer le raccourci :

```bash
mkdir -p ~/.ssh && cat >> ~/.ssh/config <<'FIN'

Host {jeton("ALIAS")}
  HostName {jeton("IP")}
  User root
  IdentityFile ~/.ssh/id_ed25519
FIN
```

5. Tester. On doit voir le nom du serveur, « Ubuntu 24.04 » et « root », sans mot de passe :

```bash
ssh {jeton("ALIAS")} 'hostname; lsb_release -ds; whoami'
```

6. Ouvrir Claude Code dans un dossier de travail pour ce client. C'est là qu'on collera tous les prompts, dans la même discussion. Quand Claude demande l'autorisation de lancer des commandes ssh, acceptez.

```bash
mkdir -p ~/Clients/{utilisateur} && cd ~/Clients/{utilisateur} && claude
```

# Étape B. Créer le sous-domaine

**Ce qu'on voit à la fin :** le sous-domaine {jeton("{DOMAINE}")} pointe vers le VPS. On le fait dès maintenant car il met parfois une heure à être pris en compte ; à l'étape 4, cette partie sera déjà faite.

Chez le fournisseur du nom de domaine (OVH, IONOS, GoDaddy…), dans la zone DNS, ajoutez cette ligne :

| Type | Nom | Valeur | TTL |
|---|---|---|---|
| A | la partie avant le domaine (ex. « agent » pour agent.monentreprise.fr) | {jeton("IP")} | 1 heure ou moins |

Pour vérifier (la commande doit afficher l'adresse IP du VPS) :

```bash
dig +short {jeton("{DOMAINE}")}
```
"""


def apres(utilisateur):
    return f"""
# Le résultat final

**Ce qu'on voit à la fin :** l'agent de l'entreprise est en ligne sur https://{jeton("{DOMAINE}")} et travaille sur ses fiches Google.

Dernière vérification, de bout en bout, connecté avec votre compte admin :
1. https://{jeton("{DOMAINE}")} affiche la page de connexion, avec le cadenas.
2. Le bureau 3D s'affiche, la pastille indique « Claude connecté ».
3. Dans la discussion, demandez « Fais l'audit de nos fiches Google » : l'agent répond en direct, au bon ton, et l'audit apparaît dans ses livrables.
4. L'onglet « Fiches Google » montre chaque établissement suivi (et la vue d'ensemble s'il y en a plusieurs).
5. Demandez une réponse à un avis : elle arrive dans « À valider », signée comme prévu ; rien n'est publié sans votre accord.
6. La page « Automatisations » contient les tâches programmées, avec leur interrupteur.

Pour donner accès à l'équipe du client, créez un compte par personne (rôle « membre » pour lire et discuter, « admin » pour tout régler) :

```bash
ssh -t {jeton("ALIAS")} 'sudo -iu {utilisateur} node app/creer-compte.js prenom@entreprise.fr "Prénom Nom" membre'
```
"""


def page(fiche):
    valeurs, a_completer = personnaliser.lire_parametres(fiche)
    champs = {k: v for k, v in CHAMPS.items() if k in ("ALIAS", "IP") or k in a_completer}
    remplis = dict(valeurs)
    for k in champs:
        remplis[k] = jeton(k)
    entreprise, utilisateur = valeurs["{ENTREPRISE}"], valeurs["{UTILISATEUR}"]

    def rendre(texte):
        texte = personnaliser.remplacer(texte, remplis)
        texte = re.sub(r"\bssh (-t )?vps\b", lambda m: f"ssh {m.group(1) or ''}{jeton('ALIAS')}", texte)
        h = build_doc.md(texte)
        h = re.sub(r'<a href="[^"]*\x00[^"]*">(.*?)</a>', r"\1", h)  # pas de lien vers une valeur encore vide
        return re.sub(r"\x00([A-Z_0-9]+)\x00", r'<span class="v" data-v="\1"></span>', h)

    corps = [rendre(avant(entreprise, utilisateur))]
    for p in sorted((ICI / "prompts").glob("*.md")):
        corps.append(rendre(re.sub(r"\A# ", "# Étape ", p.read_text(encoding="utf-8"))))
    corps.append(rendre(apres(utilisateur)))
    html_corps = "\n".join(corps)

    titres = re.findall(r"<h1>(.*?)</h1>", html_corps)
    numeros = iter(range(len(titres)))
    html_corps = re.sub(r"<h1>", lambda m: f'<h1 id="s{next(numeros)}">', html_corps)
    sommaire = "".join(f'<li><a href="#s{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in enumerate(titres))

    cases = "".join(
        f'<label>{E(lib)}<input data-champ="{k.strip("{}")}" placeholder="{E(exemple(valeurs.get(k, ""), ex))}"'
        f'{VALEUR_ALIAS if k == "ALIAS" else ""}></label>'
        for k, (lib, ex) in champs.items())

    accent = valeurs.get("{COULEUR_ACCENT}", "#FF5C2A")
    css = build_doc.CSS.replace("#FF5C2A", accent) + CSS
    titre = f"Guide complet - {entreprise}"
    return titre, f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(titre)}</title><style>{css}</style></head><body>
<span class="badge">Toog Expertise</span>
<h1 class="titre">L'agent fiche Google de {E(entreprise)} : le guide complet</h1>
<p>De la connexion au VPS du client jusqu'à l'agent en ligne. Suivez les étapes dans l'ordre. Pour chaque étape avec un prompt :
cliquez sur « Copier », collez dans Claude Code, attendez qu'il ait fini, puis vérifiez « ce qu'on voit à la fin » avant de passer à la suivante.</p>
<div class="carte" id="valeurs"><h2>Vos valeurs</h2><p>Tapez-les une fois : elles se recopient dans toutes les commandes et tous les prompts de la page (et restent enregistrées dans ce navigateur).</p>
<div class="grille">{cases}</div></div>
<h2>Sommaire</h2><ol class="sommaire">{sommaire}</ol>
{html_corps}
<div id="toast"></div>
<script>{JS}</script></body></html>"""


CSS = """
body{padding:0 16px}
.carte{background:#fff;border:1px solid #DEDACC;border-radius:14px;padding:4px 18px 16px;margin:18px 0;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}
label{font-size:9.5pt;font-weight:600;display:flex;flex-direction:column;gap:4px}
input{font:inherit;font-weight:400;padding:7px 10px;border:1px solid #DEDACC;border-radius:8px}
.v{background:#E7F6EC;border-radius:4px;padding:0 3px}
.v.vide{background:#FFE9A8;color:#7A5B00}
.prompt,.cmd{position:relative}
.copier{position:absolute;top:8px;right:10px;font:inherit;font-size:9pt;font-weight:700;border:0;border-radius:20px;padding:5px 14px;cursor:pointer;background:#FF5C2A;color:#fff}
.lab{padding-right:90px}
.sommaire a{color:inherit}
#toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#1F242E;color:#fff;padding:10px 18px;border-radius:10px;font-size:10pt;opacity:0;transition:opacity .2s;pointer-events:none;max-width:90vw}
#toast.on{opacity:1}
@media print{.copier{display:none}}
"""

JS = r"""
const champs = [...document.querySelectorAll('[data-champ]')];
const libelles = Object.fromEntries(champs.map(c => [c.dataset.champ, c.parentNode.firstChild.textContent]));
function lire(k){ try { return localStorage.getItem('guide-' + document.title + '-' + k); } catch(e) { return null; } }
function ecrire(k, v){ try { localStorage.setItem('guide-' + document.title + '-' + k, v); } catch(e) {} }
function maj(){
  for (const c of champs) {
    const v = c.value.trim();
    document.querySelectorAll(`.v[data-v="${c.dataset.champ}"]`).forEach(s => {
      s.textContent = v || '[' + libelles[c.dataset.champ].toLowerCase() + ']';
      s.classList.toggle('vide', !v);
    });
  }
}
for (const c of champs) {
  const v = lire(c.dataset.champ); if (v !== null) c.value = v;
  c.addEventListener('input', () => { ecrire(c.dataset.champ, c.value); maj(); });
}
maj();
function toast(t){ const el = document.getElementById('toast'); el.textContent = t; el.classList.add('on'); clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove('on'), 2600); }
document.querySelectorAll('.prompt,.cmd').forEach(bloc => {
  const b = document.createElement('button'); b.className = 'copier'; b.textContent = 'Copier'; bloc.appendChild(b);
  b.addEventListener('click', async () => {
    const vides = [...new Set([...bloc.querySelectorAll('.v.vide')].map(s => libelles[s.dataset.v]))];
    if (vides.length) { toast('Remplissez d\'abord en haut de la page : ' + vides.join(', ')); document.getElementById('valeurs').scrollIntoView({behavior: 'smooth'}); return; }
    const texte = bloc.querySelector('pre').innerText;
    try { await navigator.clipboard.writeText(texte); }
    catch(e) { const r = document.createRange(); r.selectNodeContents(bloc.querySelector('pre')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); document.execCommand('copy'); s.removeAllRanges(); }
    b.textContent = 'Copié ✓'; setTimeout(() => b.textContent = 'Copier', 1500);
  });
});
"""


def main():
    fiche = Path(sys.argv[1]) if len(sys.argv) > 1 else ICI / "parametres.md"
    titre, contenu = page(fiche)
    valeurs, _ = personnaliser.lire_parametres(fiche)
    nom = re.sub(r"[^a-z0-9]+", "-", valeurs.get("{ENTREPRISE}", "").lower()).strip("-") or "a-completer"
    sortie = ICI / "mes-prompts" / nom / f"{titre}.html"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(contenu, encoding="utf-8")
    print(sortie)


if __name__ == "__main__":
    main()
