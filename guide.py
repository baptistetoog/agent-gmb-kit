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

Pas besoin d'avoir déjà une clé SSH : Claude Code la crée pour vous. Il tourne sur votre ordinateur, donc la clé est créée sur votre ordinateur, et c'est elle qui ouvrira le serveur du client. Aucun compte n'est à créer pour ça : on se connecte au VPS avec l'accès root donné par l'hébergeur.

1. Ouvrir Claude Code dans un dossier de travail pour ce client (dans le Terminal de votre ordinateur). C'est là qu'on collera tous les prompts, dans la même discussion. Quand Claude demande l'autorisation de lancer des commandes, acceptez.

```bash
mkdir -p ~/Clients/{utilisateur} && cd ~/Clients/{utilisateur} && claude
```

2. Coller ce prompt : Claude crée la clé, le raccourci, et vous donne la clé publique.

```
Je vais installer un agent sur le VPS d'un client. Prépare la connexion SSH depuis cet ordinateur :
1. Si ~/.ssh/id_ed25519 n'existe pas, crée une clé SSH ed25519 (commentaire « toog-expertise », sans phrase de passe). Si elle existe déjà, garde-la. Ne touche à aucune autre clé.
2. Dans ~/.ssh/config, ajoute ce raccourci s'il n'existe pas déjà :
   Host {jeton("ALIAS")}
     HostName {jeton("IP")}
     User root
     IdentityFile ~/.ssh/id_ed25519
   Si un raccourci « {jeton("ALIAS")} » existe déjà et pointe vers une autre adresse, ne le modifie pas : arrête-toi et dis-le-moi.
3. Affiche-moi ma clé PUBLIQUE (~/.ssh/id_ed25519.pub) sur une seule ligne, puis la commande exacte à lancer moi-même pour la déposer sur le serveur.
Ne me demande jamais le mot de passe root et ne l'écris nulle part : je le taperai moi-même, dans mon terminal.
```

3. Déposer la clé sur le VPS du client (une seule fois). Deux façons, au choix :
- **Vous avez le mot de passe root** : dans un Terminal de votre ordinateur (pas dans la discussion avec Claude), lancez la commande ci-dessous, tapez « yes », puis le mot de passe root (il ne s'affiche pas pendant la frappe).
- **Le client préfère ne pas donner son mot de passe** : envoyez-lui la clé publique affichée par Claude (la ligne qui commence par ssh-ed25519). Il l'ajoute dans l'espace client de son hébergeur, rubrique « Clés SSH » (ou dans /root/.ssh/authorized_keys). La clé publique s'envoie sans risque ; le fichier id_ed25519 (sans .pub) ne se donne jamais.

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@{jeton("IP")}
```

4. Tester (dans le Terminal, ou demandez à Claude de le faire). On doit voir le nom du serveur, « Ubuntu 24.04 » et « root », sans mot de passe :

```bash
ssh {jeton("ALIAS")} 'hostname; lsb_release -ds; whoami'
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
    html_corps = "\n".join(corps).replace("<table>", '<div class="tableau"><table>').replace("</table>", "</table></div>")

    titres = re.findall(r"<h1>(.*?)</h1>", html_corps)
    numeros = iter(range(len(titres)))
    html_corps = re.sub(r"<h1>", lambda m: f'<h1 id="s{next(numeros)}">', html_corps)
    sommaire = "".join(f'<li><a href="#s{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in enumerate(titres))

    cases = "".join(
        f'<label>{E(lib)}<input data-champ="{k.strip("{}")}" placeholder="{E(exemple(valeurs.get(k, ""), ex))}"'
        f'{VALEUR_ALIAS if k == "ALIAS" else ""}></label>'
        for k, (lib, ex) in champs.items())

    accent = valeurs.get("{COULEUR_ACCENT}", "#FF5C2A")
    css = CSS.replace("--charte:#FF5C2A", f"--charte:{accent}") if re.fullmatch(r"#[0-9A-Fa-f]{6}", accent) else CSS
    titre = f"Guide complet - {entreprise}"
    return titre, f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{E(titre)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono&family=DM+Sans:wght@400;600;700&family=Lexend+Deca:wght@600&display=swap">
<style>{css}</style></head><body><main>
<span class="badge">Toog Expertise</span>
<h1 class="titre">L'agent fiche Google de {E(entreprise)} : le guide complet</h1>
<p>De la connexion au VPS du client jusqu'à l'agent en ligne. Suivez les étapes dans l'ordre. Pour chaque étape avec un prompt :
cliquez sur « Copier », collez dans Claude Code, attendez qu'il ait fini, puis vérifiez « ce qu'on voit à la fin » avant de passer à la suivante.</p>
<div class="carte" id="valeurs"><h2>Vos valeurs</h2><p>Tapez-les une fois : elles se recopient dans toutes les commandes et tous les prompts de la page (et restent enregistrées dans ce navigateur).</p>
<div class="grille">{cases}</div></div>
<h2>Sommaire</h2><ol class="sommaire">{sommaire}</ol>
{html_corps}
</main><div id="toast"></div>
<script>{JS}</script></body></html>"""


CSS = """
/* une colonne de lecture ; chaque bloc à coller est une carte avec son bouton Copier */
:root{--charte:#FF5C2A;--bg:#FAF8F4;--surface:#FFFFFF;--fg:#1F242E;--muted:#5B6070;--accent:var(--charte);
--accent-soft:color-mix(in srgb,var(--charte) 9%,#fff);--on-accent:#fff;--line:#E3DED2;--code:#F1EEE3;
--ok-bg:#E3F4E9;--ok-fg:#1E6B3A;--warn-bg:#FFE9A8;--warn-fg:#6B4F00;--badge:#FFDB21;--badge-fg:#1F242E;
--f-titre:'Lexend Deca',system-ui,sans-serif;--f-texte:'DM Sans',system-ui,sans-serif;--f-code:'DM Mono',ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#15171C;--surface:#1E2128;--fg:#ECEAE4;--muted:#A3A7B3;
--accent:color-mix(in srgb,var(--charte) 80%,#fff);--accent-soft:color-mix(in srgb,var(--charte) 14%,#1E2128);--on-accent:#15171C;
--line:#343843;--code:#2A2D36;--ok-bg:#1D3326;--ok-fg:#9BE0B4;--warn-bg:#3D3214;--warn-fg:#F5D27A;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#15171C;--surface:#1E2128;--fg:#ECEAE4;--muted:#A3A7B3;
--accent:color-mix(in srgb,var(--charte) 80%,#fff);--accent-soft:color-mix(in srgb,var(--charte) 14%,#1E2128);--on-accent:#15171C;
--line:#343843;--code:#2A2D36;--ok-bg:#1D3326;--ok-fg:#9BE0B4;--warn-bg:#3D3214;--warn-fg:#F5D27A;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--f-texte);font-size:16px;line-height:1.55;margin:0;
padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}
main{max-width:820px;margin:0 auto}
h1{font-family:var(--f-titre);font-weight:600;font-size:1.55rem;line-height:1.25;text-wrap:balance;margin:48px 0 8px;padding-top:14px;border-top:3px solid var(--accent)}
h1.titre{border:none;font-size:2.1rem;margin-top:12px;padding-top:0}
h2{font-family:var(--f-titre);font-weight:600;font-size:1.1rem;color:var(--accent);margin:24px 0 8px}
p,li{max-width:68ch}
a{color:var(--accent)}
.badge{display:inline-block;background:var(--badge);color:var(--badge-fg);font-weight:700;font-size:.75rem;padding:3px 10px;border-radius:20px}
.prompt,.cmd{position:relative;border-radius:12px;padding:12px 16px;margin:12px 0;min-width:0}
.prompt{background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
.cmd{background:var(--surface);border:1px solid var(--line)}
.lab{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;color:var(--accent);padding-right:96px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-family:var(--f-code);font-size:.85rem;line-height:1.5;margin:0}
code{font-family:var(--f-code);font-size:.88em;background:var(--code);padding:1px 5px;border-radius:5px;overflow-wrap:anywhere}
.tableau{overflow-x:auto}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:.9rem}
th,td{border:1px solid var(--line);padding:7px 9px;text-align:left;vertical-align:top}
th{background:var(--code)}
.carte{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:4px 18px 18px;margin:20px 0}
.grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
label{font-size:.8rem;font-weight:600;display:flex;flex-direction:column;gap:5px;min-width:0}
input{font:inherit;font-size:.92rem;font-weight:400;padding:8px 11px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);min-width:0}
input:focus-visible,.copier:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.v{background:var(--ok-bg);color:var(--ok-fg);border-radius:4px;padding:0 3px}
.v.vide{background:var(--warn-bg);color:var(--warn-fg)}
.copier{position:absolute;top:9px;right:10px;font:inherit;font-size:.78rem;font-weight:700;border:0;border-radius:20px;padding:6px 15px;cursor:pointer;background:var(--accent);color:var(--on-accent)}
.sommaire a{color:inherit}
#toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--fg);color:var(--bg);padding:10px 18px;border-radius:10px;font-size:.9rem;opacity:0;transition:opacity .2s;pointer-events:none;max-width:calc(100vw - 32px)}
#toast.on{opacity:1}
@media (prefers-reduced-motion:reduce){#toast{transition:none}}
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
