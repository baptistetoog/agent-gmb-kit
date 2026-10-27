# Kit agent fiche Google : un agent IA pour n'importe quelle entreprise

Ce kit installe, en 14 prompts collés dans Claude Code, un agent IA qui gère les fiches Google Business Profile d'une entreprise. Il fonctionne pour un seul établissement comme pour un réseau (franchise, agences, parcs, magasins…), et pour tout type d'activité.

L'outil obtenu : une page de connexion protégée, le bureau 3D de l'agent, une discussion en direct, sa mémoire, ses skills, la connexion aux fiches via Activepieces, les validations « Propose / Agit seul », un tableau de bord des fiches (avec une vue d'ensemble s'il y a plusieurs établissements), le site et la photothèque, les automatisations, et l'atelier où l'agent améliore son propre outil.

Tout ce qui change d'une entreprise à l'autre (nom, activité, périmètre, ton, personnage, charte graphique) se règle dans **une seule fiche de paramètres**. Les prompts, eux, ne changent pas.

## Les liens

- Dépôt du kit : https://github.com/baptistetoog/agent-gmb-kit
- Scène 3D téléchargée par le prompt 5 : https://raw.githubusercontent.com/baptistetoog/agent-gmb-kit/main/kit/bureau3d.js
- Démo en ligne de l'outil (instance de test) : https://gmb-demo.toog-expertise.app
- Toog Expertise : https://toog-expertise.app

## Utilisation

1. Copier `parametres.md` (ou partir d'un exemple de `exemples/`) et remplir la colonne « Valeur ».
2. Lancer :
   ```bash
   python3 personnaliser.py exemples/newjump.md
   ```
   Les 14 prompts personnalisés et le document HTML sont créés dans `mes-prompts/<entreprise>/`. Le script signale ce qui reste à compléter.
3. Coller les prompts dans Claude Code, dans l'ordre, un par un, en vérifiant « ce qu'on voit à la fin » avant de passer au suivant.

## Avant de commencer

- Un VPS Ubuntu 24.04 accessible depuis Claude Code par `ssh vps`.
- Un nom de domaine, dont on crée un sous-domaine.
- Un abonnement Claude (Pro ou Max).
- Un compte Activepieces avec une connexion Google My Business, reliée au compte Google qui gère la ou les fiches.

## Les paramètres qui adaptent l'agent

| Paramètre | Ce qu'il change |
|---|---|
| `{ACTIVITE}` | les rubriques de la fiche d'identité de l'entreprise, les exemples des skills, le calendrier des posts |
| `{ETABLISSEMENTS}` | le périmètre : un établissement, ou plusieurs (sélecteur, vue d'ensemble, garde qui bloque les fiches hors périmètre, automatisations par établissement) |
| `{TON}`, `{SIGNATURE}`, `{MOMENT_CLIENT}` | la façon dont l'agent parle, signe les réponses aux avis et demande des avis |
| `{NOM_AGENT}`, `{COULEUR_AGENT}`, `{COULEUR_YEUX}`, `{BADGE}`, `{ACCESSOIRE}` | le personnage du bureau 3D |
| `{COULEUR_FOND}`, `{COULEUR_ACCENT}`, `{COULEUR_ACCENT_2}`, `{COULEUR_TEXTE}`, `{POLICE_TITRES}`, `{POLICE_TEXTE}`, `{LOGO}`, `{CHARTE_CONSIGNES}` | la charte de l'outil : toutes les couleurs sont définies dans un seul bloc de `design.css`, faciles à changer plus tard |

Les paramètres sont recopiés dans la section « Paramètres » du `PROJET.md` de l'instance au prompt 3, et toutes les étapes suivantes s'y réfèrent.

## Les prompts

| # | Chapitre | Fichier | À la main |
|---|---|---|---|
| 1 | Préparer l'espace de l'agent sur le serveur | `prompts/01-espace-serveur.md` | — |
| 2 | Créer la clé de connexion à Claude | `prompts/02-connecter-claude.md` | `claude setup-token` |
| 3 | Créer l'outil et son espace de connexion protégé | `prompts/03-outil-connexion.md` | — |
| 4 | Mettre l'outil en ligne sur son sous-domaine | `prompts/04-mise-en-ligne.md` | DNS + son compte admin |
| 5 | Donner vie à l'agent : bureau, discussion, cerveau | `prompts/05-agent-visuel.md` | coller la clé dans « Connecter Claude » |
| 6 | La fiche de l'agent et sa mémoire | `prompts/06-fiche-memoire.md` | — |
| 7 | Les skills | `prompts/07-skills.md` | — |
| 8 | Les connexions : API et MCP (Activepieces) | `prompts/08-connexions.md` | clic sur « Connecter » |
| 9 | « Propose » ou « agit seul » : les validations | `prompts/09-validations.md` | — |
| 10 | Le tableau de bord des fiches Google | `prompts/10-tableau-de-bord.md` | confirmer les établissements |
| 11 | Le site internet et les photos | `prompts/11-site-photos.md` | déposer ses photos |
| 12 | Les automatisations | `prompts/12-automatisations.md` | répondre à l'entretien de l'agent |
| 13 | L'agent ajoute des fonctionnalités à son outil | `prompts/13-atelier.md` | — |
| 14 | Option : parler à son agent | `prompts/14-vocal.md` | — |

## Le contenu du dépôt

- `prompts/` : les 14 prompts génériques, avec leurs variables entre accolades.
- `parametres.md` : la fiche de paramètres à remplir. `exemples/` : des fiches déjà remplies (NewJump, réseau de parcs).
- `personnaliser.py` : fabrique les prompts et le document d'une entreprise. `build_doc.py` : le document du kit générique (`livrable/`).
- `kit/bureau3d.js` : la scène 3D du bureau (personnage paramétrable : nom, couleurs, badge, accessoire, fond). Les prompts la téléchargent directement depuis ce dépôt : il doit donc être public.
- `outils/` : pour le formateur. `enregistrer-etape.sh` enregistre le code d'une instance de test après chaque prompt (étiquettes `etape-NN`) et `construire-public.sh` en tire le dépôt public, sans donnée client ni secret.

## Code de référence par étape

Les prompts « Si vous êtes vraiment bloqué » remettent l'outil à l'état de l'étiquette `etape-NN` de ce dépôt. Ces étiquettes s'obtiennent en passant les 14 prompts sur une instance de test et en lançant `outils/enregistrer-etape.sh` après chacun, puis `outils/construire-public.sh`.
