# 3. Créer l'outil et son espace de connexion protégé

**Ce qu'on voit à la fin :** l'outil tourne sur le serveur, avec une page de connexion. Seules les personnes qui ont un compte peuvent entrer.

---

```
Mon serveur est accessible par `ssh vps` (root). Le projet appartient à l'utilisateur Linux {UTILISATEUR}, qui a déjà Node 22 et Claude Code.

Je veux créer l'outil web de mon agent IA, pour l'entreprise {ENTREPRISE}. Commence par la base : le serveur et l'espace de connexion protégé.

Voici les paramètres du projet. Toutes les étapes suivantes s'y réfèrent : recopie-les tels quels dans une section « Paramètres » de PROJET.md (voir plus bas).
- Entreprise : {ENTREPRISE} — site : {SITE_WEB} — activité : {ACTIVITE}
- Périmètre (établissements gérés par l'agent) : {ETABLISSEMENTS}
- Ton : {TON} — signature des réponses aux avis : {SIGNATURE} — on demande un avis après : {MOMENT_CLIENT}
- Agent : {NOM_AGENT} (corps {COULEUR_AGENT}, yeux {COULEUR_YEUX}, badge « {BADGE} », accessoire : {ACCESSOIRE})
- Charte : fond {COULEUR_FOND}, accent {COULEUR_ACCENT}, accent secondaire {COULEUR_ACCENT_2}, texte {COULEUR_TEXTE}, police des titres « {POLICE_TITRES} », police du texte « {POLICE_TEXTE} » (Google Fonts), logo : {LOGO}, consignes en plus : {CHARTE_CONSIGNES}

Organisation des dossiers (dans /home/{UTILISATEUR}) :
- app/ : le code de l'outil (serveur + pages)
- data/ : les données privées (comptes, sessions, historique, connexions), droits 700
- agent/ : le dossier de travail de l'agent (on le remplira plus tard)
- PROJET.md : la mémoire du projet (voir plus bas)

Le serveur :
- Un seul fichier app/server.js en Node.js 22, SANS aucune dépendance npm (uniquement les modules intégrés : http, crypto, fs, path, child_process…).
- Il écoute seulement sur 127.0.0.1:{PORT} (nginx sera devant plus tard).
- Il sert les pages du dossier app/public/.

L'espace de connexion :
- Page app/public/connexion.html : e-mail + mot de passe, sobre, propre, adaptée au mobile. Elle suit la charte des paramètres : fond {COULEUR_FOND}, bouton et accents {COULEUR_ACCENT}, texte {COULEUR_TEXTE}, titres en « {POLICE_TITRES} », texte en « {POLICE_TEXTE} » (Google Fonts). En haut, le logo ({LOGO} ; si « aucun », un carré arrondi couleur accent avec l'initiale de l'entreprise) et le nom de l'entreprise.
- Les comptes sont dans data/comptes.json : e-mail, nom, rôle (« admin » ou « membre »), mot de passe haché avec crypto.scrypt et un sel unique (jamais en clair).
- Session par cookie : HttpOnly, Secure, SameSite=Lax, valable 30 jours, sessions stockées dans data/sessions.json.
- Après 5 mauvais mots de passe en 15 minutes pour la même adresse IP, on bloque 15 minutes.
- Toute page ou API (sauf la page de connexion et ses fichiers) renvoie vers la connexion si on n'est pas connecté.
- Bouton « Se déconnecter ».
- Un petit script app/creer-compte.js pour créer ou modifier un compte en ligne de commande :
  `node app/creer-compte.js email@exemple.fr "Prénom Nom" admin`
  Il demande le mot de passe sans l'afficher (deux fois). Il accepte aussi une variable d'environnement MOT_DE_PASSE pour les tests automatiques, et une option --supprimer pour retirer un compte (ses sessions sont fermées).
- Une fois connecté, la page app/public/index.html affiche pour l'instant : « Bonjour <prénom>, ton agent arrive bientôt. »

Le service :
- Un service systemd nommé {UTILISATEUR}-app qui lance le serveur en tant que {UTILISATEUR}, redémarre tout seul en cas d'arrêt et démarre avec le serveur. Ajoute les protections systemd simples : NoNewPrivileges, PrivateTmp, ProtectSystem=strict avec écriture autorisée seulement dans /home/{UTILISATEUR}.
- Le service charge le fichier /home/{UTILISATEUR}/.claude-token.env s'il existe (on s'en servira pour l'agent).

PROJET.md : écris-y en français simple la section « Paramètres » (ci-dessus), l'organisation des dossiers, comment démarrer/arrêter/voir les journaux du service, et ce qui a été fait à cette étape. À chaque étape suivante, on le relira avant de commencer et on le mettra à jour à la fin.

Vérifications à faire toi-même avant de me rendre la main :
- le service tourne (systemctl status) ;
- sans être connecté, `curl` sur / renvoie vers la page de connexion ;
- crée un compte de test avec creer-compte.js (MOT_DE_PASSE en variable), connecte-toi avec curl, vérifie que la page d'accueil répond, puis supprime ce compte de test ;
- les fichiers de data/ ne sont lisibles que par {UTILISATEUR}.

Ne touche à aucun autre site, service ou utilisateur du serveur. À la fin, donne-moi la commande exacte pour créer mon propre compte admin.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 3, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 3 du dépôt {DEPOT} (étiquette etape-03) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
