# 5. Donner vie à l'agent : son bureau, la discussion, son cerveau

**Ce qu'on voit à la fin :** après connexion, on arrive dans le bureau de l'agent. On voit son personnage et on lui parle comme dans une messagerie. Il répond en direct et on voit ce qu'il est en train de faire.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md.

Remplace la page d'accueil provisoire par le bureau de l'agent, et branche son cerveau (Claude Code).

LE CERVEAU (côté serveur, dans app/server.js ou un fichier app/agent.js) :
- L'agent travaille dans le dossier /home/{UTILISATEUR}/agent. Chaque message lance :
  `claude -p --output-format stream-json --verbose --include-partial-messages --model sonnet --setting-sources project --strict-mcp-config` avec le message en entrée, dans ce dossier, en tant que {UTILISATEUR}.
  Le binaire est ~/.local/bin/claude. Le jeton est passé dans la variable CLAUDE_CODE_OAUTH_TOKEN, lue dans /home/{UTILISATEUR}/.claude-token.env à CHAQUE lancement (pas seulement au démarrage du service).
- LA CASE « CONNECTER CLAUDE » (admin) : dans le bureau, un bouton « Connecter Claude » ouvre une fenêtre avec un champ masqué où l'on colle la clé obtenue avec `claude setup-token`. Le serveur :
  - nettoie la saisie (espaces, retours à la ligne, guillemets, préfixe « CLAUDE_CODE_OAUTH_TOKEN= » ou « export » collés par erreur, clé collée deux fois) et vérifie qu'elle commence par sk-ant-oat01- ;
  - la teste en lançant `claude -p "Réponds seulement : prêt"` avec cette clé ;
  - si la réponse est bonne, l'enregistre dans .claude-token.env (droits 600) et affiche « ✅ Claude est connecté » ; sinon, n'enregistre rien et affiche une erreur claire (« Clé refusée par Claude : refaites claude setup-token »).
  - La clé n'est jamais renvoyée au navigateur ni écrite dans les journaux.
  - En haut du bureau, une pastille indique en permanence « Claude connecté » (vert) ou « Claude non connecté » (orange, cliquable pour ouvrir la fenêtre). Si un membre non admin envoie un message alors que Claude n'est pas connecté, il voit « L'agent n'est pas encore connecté : demandez à un admin ».
- Variables d'environnement à ajouter pour chaque lancement : ENABLE_CLAUDEAI_MCP_SERVERS=false et DISABLE_AUTOUPDATER=1.
- Outils autorisés (--allowedTools) : Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Skill. Interdits (--disallowedTools) : Bash, Task, Agent, NotebookEdit.
- Crée agent/.claude/settings.json (avec "disableAllHooks": true) pour lui interdire, avec des règles permissions.deny de Claude Code de type Read(...) et Edit(...) (Edit couvre aussi l'écriture : pas de règles Write) :
  - de lire ou modifier /home/{UTILISATEUR}/data, /home/{UTILISATEUR}/app, ~/.claude-token.env, ~/.claude, ~/.claude.json et /proc (sinon il pourrait lire le jeton dans /proc/self/environ) ;
  - de modifier sa propre configuration : agent/CLAUDE.md, agent/.claude/settings.json, agent/.claude/settings.local.json et agent/.mcp.json.
  - de modifier les fichiers cachés et les .md à la racine de /home/{UTILISATEUR} (~/.bashrc, ~/.profile, ~/.local/ qui contient le programme claude…) : sinon il pourrait réécrire claude et contourner l'interdiction de Bash.
  Il garde le droit d'écrire partout ailleurs dans agent/ (y compris agent/.claude/skills/, dont on se servira plus tard).
- Écris un agent/CLAUDE.md provisoire de quelques lignes : il s'appelle « {NOM_AGENT} », agent IA de {ENTREPRISE} ({ACTIVITE}) pour les fiches Google Business Profile ({ETABLISSEMENTS}), il répond en français sur ce ton : {TON}, il ne sort jamais de son dossier. (On écrira sa vraie fiche à l'étape suivante.)
- Tous les fichiers de agent/ appartiennent à {UTILISATEUR} (l'outil devra pouvoir les modifier). Ce sont les règles ci-dessus, pas les droits Linux, qui protègent la configuration : ne redonne donc jamais Bash à l'agent.
- Une discussion continue : garde le session_id renvoyé par Claude et utilise --resume pour les messages suivants. Bouton « Nouvelle discussion » pour repartir de zéro.
- Un seul travail à la fois. Si un message arrive pendant que l'agent travaille, il est mis en file d'attente. Bouton « Arrêter » qui coupe le travail en cours.
- Limite de sécurité : 10 minutes maximum par message.
- Historique enregistré dans data/historique.jsonl (qui a parlé, quand, le texte, les outils utilisés, la durée, le coût estimé renvoyé par Claude).
- Le temps réel vers la page se fait en Server-Sent Events : statut de l'agent (au repos / réfléchit / utilise un outil : lequel / a fini), morceaux de réponse, fin.

L'INTERFACE : je veux une vraie application, belle et vivante, où l'on VOIT l'agent travailler. Pas une page de formulaire. Sans framework ni étape de compilation : HTML + CSS + JavaScript (modules), avec three.js (pour la scène 3D) chargé par une importmap depuis https://cdn.jsdelivr.net/npm/three@0.170.0/. Adapte la politique de sécurité du contenu (CSP) du serveur pour autoriser seulement ce qu'il faut : cdn.jsdelivr.net pour les scripts, Google Fonts pour les polices.

1. LE SYSTÈME DE DESIGN (app/public/design.css, utilisé par toutes les pages, y compris la connexion et toutes celles des étapes suivantes). Il applique la charte de la section « Paramètres » de PROJET.md :
   - Couleurs en variables CSS, toutes définies UNE SEULE FOIS en haut de design.css (:root) pour qu'on puisse changer la charte en modifiant ce seul bloc : --fond {COULEUR_FOND}, --surface (blanc, ou une teinte très claire du fond si le fond est sombre), --texte {COULEUR_TEXTE}, --texte-2 (texte secondaire, une version adoucie du texte), --accent {COULEUR_ACCENT}, --accent-pale (l'accent très éclairci, pour mes bulles de discussion), --accent-2 {COULEUR_ACCENT_2}, --vert #2E9E6A, --rouge #D9443B, --bordure (une teinte légèrement plus foncée que le fond). Le texte posé sur l'accent doit rester lisible (contraste AA) : blanc ou texte foncé selon la couleur d'accent.
   - Polices Google Fonts : « {POLICE_TITRES} » pour les titres, « {POLICE_TEXTE} » pour le texte.
   - Logo : {LOGO} (si « aucun », un carré arrondi couleur accent avec l'initiale de l'entreprise). S'il s'agit d'une adresse externe, recopie le fichier dans app/public/ plutôt que de le charger depuis un autre site.
   - Consignes de charte en plus : {CHARTE_CONSIGNES}.
   - Cartes blanches arrondies (16 px) avec une ombre douce, boutons « pilule » (orange plein pour l'action principale, contour pour les autres), pastilles d'état (point de couleur + texte), champs arrondis, focus visible, transitions de 150 ms.
   - Composants réutilisables : .carte, .bouton, .bouton-secondaire, .pastille, .onglets, .fenetre (modale), .toast (message éphémère), .vide (état vide avec illustration et phrase d'aide), .squelette (chargement).

2. LA SCÈNE DU BUREAU : elle est fournie toute prête dans le dépôt du kit ({DEPOT}). Télécharge-la directement sur le serveur depuis {DEPOT_BRUT}/kit/bureau3d.js et enregistre-la TELLE QUELLE dans /home/{UTILISATEUR}/app/public/bureau3d.js, sans la modifier. Lis le commentaire en tête du fichier : il explique comment l'utiliser.
   - Dans l'interface : const bureau = creerBureau(conteneur, { nom: "{NOM_AGENT}", entreprise: <nom de l'entreprise>, couleurCorps: "{COULEUR_AGENT}", couleurYeux: "{COULEUR_YEUX}", badge: "{BADGE}", accessoire: "{ACCESSOIRE}", fond: "{COULEUR_FOND}" }).
   - Branche-le sur les événements en temps réel de l'agent : bureau.statut("message") quand on envoie un message, "reflechit" quand il réfléchit, "outil" avec le texte de ce qu'il fait (ex. « Je lis la fiche Google… ») quand il utilise un outil, "repond" pendant qu'il écrit sa réponse, "fini" à la fin, "repos" sinon.
   - L'importmap de la page doit pointer « three » vers https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js et « three/addons/ » vers https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/.

3. LA DISPOSITION :
   - Sur ordinateur : la scène à gauche (environ 55 % de la largeur, pleine hauteur) et, à droite, un panneau avec des onglets « Discussion » (et, aux étapes suivantes, « Fiches Google », « À valider », « Réglages »). Au-dessus de la scène, une étiquette flottante : nom de l'agent, rôle et ce qu'il fait en ce moment.
   - Sur mobile : la scène en haut (environ 40 % de l'écran, repliable), le panneau en dessous, et une barre d'onglets en bas de l'écran avec des icônes. L'en-tête tient sur une ligne : logo, pastille de connexion, menu ☰.
   - Le nom de l'entreprise n'est écrit en dur nulle part : il vient de la variable NOM_ENTREPRISE du service systemd (Environment="NOM_ENTREPRISE={ENTREPRISE}", entre guillemets à cause des espaces), exposée aux pages (et à la page de connexion par une petite route publique /api/marque).
   - En-tête fin : logo, nom de l'entreprise, pastille « Claude connecté », prénom de la personne connectée, déconnexion.

4. LA DISCUSSION :
   - bulles façon messagerie (les miennes à droite en orange pâle, celles de l'agent à gauche en blanc, avec sa petite tête), heure, réponse en Markdown (titres, listes, gras, liens, tableaux) ;
   - la réponse s'écrit en direct ; pendant le travail, une ligne discrète montre les outils utilisés (« 🔧 Lit la fiche », dépliable) ;
   - zone de saisie arrondie qui grandit avec le texte (Entrée = envoyer, Maj+Entrée = retour à la ligne), boutons « Arrêter » (visible seulement pendant le travail) et « Nouvelle discussion » ;
   - état vide accueillant : la tête de l'agent, « Bonjour, je suis {NOM_AGENT} » et 3 suggestions cliquables ;
   - l'historique revient au rechargement.

5. LA MISE EN ROUTE (pour que la personne voie tout de suite où elle en est et que le système fonctionne) :
   - Tant que tout n'est pas prêt, une carte « Mise en route » est ÉPINGLÉE en haut de l'onglet Discussion (au-dessus du fil des messages, pas dedans : elle ne doit jamais disparaître en faisant défiler). Elle est dépliée par défaut, y compris sur mobile (plus compacte), et se redéplie toute seule dès qu'une étape est franchie. Elle contient des étapes cochées en direct :
     1) Connecter Claude (bouton « Connecter Claude ») ;
     2) Connecter la fiche Google via Activepieces ;
     3) Choisir le ou les établissements (selon le périmètre des paramètres) ;
     4) Première lecture des fiches et des avis.
     Les étapes 2 à 4 s'affichent « Bientôt disponible » tant que leur fonction n'est pas installée (elles arrivent aux étapes suivantes de l'installation) : la carte lit pour cela un petit état fourni par le serveur (GET /api/etat).
   - Dans un onglet « Réglages » : une section « État du système » avec des voyants (Claude, Google/Activepieces, dernière lecture de la fiche, prochaine automatisation), toujours visible même une fois la mise en route terminée.

Vérifie toi-même, de bout en bout : connecte-toi avec un compte de test (créé puis supprimé à la fin), envoie « Bonjour, présente-toi en une phrase » par l'API, vérifie que la réponse arrive en temps réel, qu'elle est enregistrée, et qu'un deuxième message se souvient du premier. Vérifie que l'agent ne peut pas lire data/comptes.json (demande-lui, il doit refuser ou échouer). Mets à jour PROJET.md.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 5, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 5 du dépôt {DEPOT} (étiquette etape-05) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
