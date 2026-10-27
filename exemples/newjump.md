# Paramètres de l'agent — exemple NewJump (réseau de parcs)

Les couleurs, les polices et le logo sont encore ceux de la démo : remplacez-les par la charte NewJump avant de lancer `python3 personnaliser.py exemples/newjump.md`.

Remplissez la colonne « Valeur » une fois, puis lancez `python3 personnaliser.py` (ou `python3 personnaliser.py exemples/mon-fichier.md`).
Le script recopie les 14 prompts dans `mes-prompts/` avec vos valeurs, prêts à coller dans Claude Code, et fabrique le document `mes-prompts/Prompts - <entreprise>.html`.

Une valeur laissée à « À compléter » est signalée par le script. Les valeurs déjà remplies sont celles de la démo : elles fonctionnent telles quelles.

## Le serveur

| Variable | Valeur | Ce que c'est |
|---|---|---|
| {DOMAINE} | À compléter (ex. agent.newjump.fr) | le sous-domaine de l'outil (ex. agent.monentreprise.fr) |
| {UTILISATEUR} | newjump | l'utilisateur Linux du projet, en minuscules sans espace (ex. monentreprise) |
| {PORT} | 4900 | le port interne de l'outil (un port libre sur le serveur) |
| {EMAIL_ADMIN} | À compléter | votre e-mail de connexion à l'outil |
| {DEPOT} | https://github.com/baptistetoog/agent-gmb-kit | le dépôt GitHub du kit (scène 3D et code de référence) |

## L'entreprise

| Variable | Valeur | Ce que c'est |
|---|---|---|
| {ENTREPRISE} | NewJump | le nom de l'entreprise ou de l'enseigne, tel qu'affiché aux clients |
| {SITE_WEB} | À compléter | l'adresse du site (ex. https://www.monentreprise.fr) |
| {ACTIVITE} | À compléter | l'activité en une phrase (ex. « parc de loisirs indoor pour enfants et adultes », « plombier chauffagiste », « restaurant italien ») |
| {MOMENT_CLIENT} | la visite au parc | le moment après lequel on demande un avis (ex. « la séance », « l'intervention », « le repas », « l'achat ») |
| {ETABLISSEMENTS} | tous les parcs du réseau NewJump, chacun avec sa propre fiche Google : l'agent les gère tous, parc par parc, et donne aussi une vue d'ensemble du réseau | LA CONSIGNE DE PÉRIMÈTRE, en clair. Ex. « un seul établissement » ; « tous les parcs du réseau, chacun avec sa fiche Google » ; « les 3 agences de Marseille, Aix et Toulon » |
| {TON} | À compléter (ex. tutoiement, fun et dynamique) | le ton de l'agent et des textes publiés (ex. « tutoiement, fun et dynamique ») |
| {SIGNATURE} | L'équipe {ENTREPRISE} suivie du nom du parc (ex. « L'équipe NewJump Lyon ») | la signature des réponses aux avis (ex. « L'équipe {ENTREPRISE} suivie du nom de l'établissement » pour signer au nom de chaque établissement) |

## L'agent (son personnage dans le bureau 3D)

| Variable | Valeur | Ce que c'est |
|---|---|---|
| {NOM_AGENT} | La Cartographe | son nom |
| {COULEUR_AGENT} | #2F4A3A | la couleur de son corps |
| {COULEUR_YEUX} | #F2C14E | la couleur de ses yeux |
| {BADGE} | GMB | le texte du badge sur sa poitrine (4 caractères maximum) |
| {ACCESSOIRE} | lanterne | lanterne, loupe, casque ou aucun |

## La charte graphique de l'outil

| Variable | Valeur | Ce que c'est |
|---|---|---|
| {COULEUR_FOND} | #FBF7F0 | le fond des pages |
| {COULEUR_ACCENT} | #FF5C2A | la couleur principale (boutons, liens, onglet actif) |
| {COULEUR_ACCENT_2} | #FFDB21 | la couleur secondaire (badges, mises en avant) |
| {COULEUR_TEXTE} | #1F1A17 | la couleur du texte |
| {POLICE_TITRES} | Lexend Deca | la police des titres (nom exact sur Google Fonts) |
| {POLICE_TEXTE} | DM Sans | la police du texte (nom exact sur Google Fonts) |
| {LOGO} | aucun | l'adresse d'un logo (PNG ou SVG) ; « aucun » = un carré de couleur avec l'initiale |
| {CHARTE_CONSIGNES} | aucune | consignes de charte en plus, en clair (ex. « coins plus arrondis, style ludique, pas de noir pur ») |
