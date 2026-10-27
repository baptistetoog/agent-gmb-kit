# 10. Le tableau de bord des fiches Google

**Ce qu'on voit à la fin :** un onglet « Fiches Google » dans l'outil. Avec plusieurs établissements, on choisit l'établissement en haut (ou « Vue d'ensemble »). On y trouve l'état de la fiche, les nouveaux avis avec un bouton « Répondre », les posts avec un bouton « Nouveau post », et les ajustements conseillés avec un bouton « Appliquer ». Chaque bouton confie une mission à l'agent. Tout ce qui modifie la fiche passe par une carte « À valider ».

**Prérequis :** Activepieces connecté (étape 8), avec la pièce Google My Business.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Je veux un tableau de bord simple des fiches Google Business de l'entreprise, que l'agent alimente et sur lequel on agit en un clic. Périmètre (voir « Paramètres » dans PROJET.md) : {ETABLISSEMENTS}. Tout ce qui suit doit marcher aussi bien avec un seul établissement qu'avec plusieurs : avec un seul, on ne montre ni sélecteur ni vue d'ensemble.

LES DONNÉES (l'agent les récupère avec Activepieces, l'outil les affiche) :
- Avec Activepieces, l'agent lit et agit sur la fiche par ap_run_action, avec pieceName « @activepieces/piece-google-my-business », l'externalId de la connexion Google (donné par ap_list_connections) et l'actionName :
  - lire : list-accounts → list-locations → get-location, list-reviews, list-posts (ap_get_piece_props donne les champs d'entrée de chaque action) ;
  - répondre à un avis : reply-to-review ; publier : create-post ; modifier la fiche : update-location (toujours après validation en mode « Propose »).
  Activepieces refuse un ap_run_action sans champ input : toujours le passer ({} si vide).
  Limite d'Activepieces : update-location ne modifie que le site web, les libellés et le code de magasin. Pour la description, le téléphone, les horaires, l'adresse et les catégories, l'agent prépare la valeur exacte et indique qu'une personne doit la saisir dans Google Business Profile.
  Écris ce mode d'emploi dans agent/CLAUDE.md et dans les skills concernés.
- Ajoute à app/mcp-plateforme.js l'outil tableau_enregistrer(etablissement, section, donnees), avec 4 sections :
  - « fiche » : les champs principaux + un score sur 100 ;
  - « avis » : la liste (id, auteur, note, texte, date, réponse existante) ;
  - « posts » : la liste des derniers posts ;
  - « ajustements » : la liste (id, champ, valeur actuelle, valeur proposée, pourquoi).
  Le serveur vérifie le format et que l'établissement fait partie des établissements choisis, ajoute la date et enregistre dans data/gmb/<identifiant de l'établissement>/<section>.json.
- Ajoute aussi tableau_lire(etablissement, section, id) pour retrouver un avis ou un ajustement par son identifiant.
- La première fois, l'agent repère le ou les comptes et les établissements (list-accounts puis list-locations), et propose ceux qui correspondent au périmètre, en les rapprochant de la rubrique « Établissements » de ENTREPRISE.md. Un admin confirme la liste. Comme l'agent n'a pas le droit de modifier ENTREPRISE.md, ajoute l'outil noter_etablissements(liste de {compte, etablissement, nom, connexion}) qui écrit seulement une section « Fiches Google (identifiants) » dans ce fichier (un tableau : nom, identifiant d'établissement, compte, connexion Activepieces) et enregistre la même liste dans data/gmb/etablissements.json. Un admin peut retirer ou rajouter un établissement depuis Réglages → Connexions.
- La garde (serveur MCP d'approbation) refuse toute lecture ou action qui vise un établissement absent de cette liste. Tant que la liste est vide, seuls list-accounts et list-locations sont libres.

MISE EN ROUTE : les étapes 3 et 4 deviennent actives. Dès que la connexion activepieces est faite, le tri de ses outils (lecture libre / action à valider) est fait automatiquement, sans attendre qu'un admin clique sur « Tester », pour que l'agent puisse lire la fiche tout de suite. Étape 3 « Choisir les établissements » : bouton qui demande à l'agent de repérer les comptes et les établissements et de proposer la liste ; l'admin la confirme dans une carte (cases à cocher, tout coché par défaut pour ceux du périmètre). Étape 4 « Première lecture » : bouton qui lance « Actualiser » pour tous les établissements choisis. Quand les 4 étapes sont faites, la carte affiche « ✅ Votre agent est opérationnel », avec le nombre d'établissements suivis, le nombre d'avis trouvés et le nombre d'avis sans réponse, puis disparaît au rechargement suivant.

L'ONGLET « FICHES GOOGLE » (onglet du panneau à côté de « Discussion » ; sur mobile, dans la barre d'onglets en bas ; avec le système de design design.css) :
- S'il y a plusieurs établissements : en haut, un sélecteur (liste déroulante avec recherche s'il y en a plus de 8) avec « Vue d'ensemble » puis chaque établissement. Le choix est gardé dans le navigateur.
  - « Vue d'ensemble » : un tableau d'une ligne par établissement (nom, note, nombre d'avis, avis sans réponse, score de la fiche, date du dernier post), triable, avec une pastille rouge sur les avis sans réponse ; un clic sur une ligne ouvre l'établissement. Bouton « Actualiser tout » (mission : « Actualise le tableau de bord de tous les établissements, un par un. »).
- Pour un établissement : en haut, son nom, sa note moyenne, son nombre d'avis, le score de la fiche sur 100, la date de mise à jour, et un bouton « Actualiser » (mission : « Actualise le tableau de bord de <nom> : fiche, avis, posts et ajustements. »).
- « Avis » : du plus récent au plus ancien, ceux sans réponse en premier avec une pastille « Nouveau ». Bouton « Répondre » sur chacun (mission : « Rédige une réponse à l'avis <id> de <nom> avec le skill reponse-avis, puis demande la validation pour la publier. »).
- « Posts » : les derniers posts, et un bouton « Nouveau post » avec un petit formulaire (sujet, type : actu / offre / événement / conseil ; avec plusieurs établissements, une case « Décliner pour tous les établissements » qui confie la mission pour chacun). Mission : rédiger avec le skill post-google, puis demander la validation pour publier.
- « Ajustements conseillés » : chaque ajustement a un bouton « Appliquer » (mission : « Applique l'ajustement <id> sur la fiche de <nom>, après validation. ») et un bouton « Ignorer ».
- Les cartes « À valider » indiquent toujours l'établissement concerné, en évidence.
- Une mission lancée depuis un bouton apparaît aussi dans la discussion. L'onglet se met à jour en direct (SSE) quand l'agent enregistre des données.
- Quand il n'y a pas encore de données : « Cliquez sur Actualiser ».

LES SKILLS (dans agent/.claude/skills/) :
- Ajoute « appliquer-ajustement » : préparer la modification exacte (action update-location, champs et nouvelles valeurs), demander la validation avec ce contenu exact, puis, une fois validé, l'exécuter et relire la fiche pour confirmer.
- Mets à jour « audit-fiche » : à la fin, enregistrer le score dans « fiche » et les manques dans « ajustements » avec tableau_enregistrer.
- Mets à jour « reponse-avis » : réponse naturelle, jamais deux fois la même formule, prénom de l'auteur si disponible (sauf préférence contraire dans la mémoire), un détail précis repris de l'avis, signature tirée de la mémoire.

Dans agent/CLAUDE.md, section « Ton tableau de bord » : après chaque lecture de données Google, il appelle tableau_enregistrer pour l'établissement concerné. Quand on lui demande « tous les établissements », il les traite un par un, dans l'ordre de la liste, et termine par une synthèse courte. Toute réponse à un avis, toute publication et toute modification de la fiche passent par demander_validation (en mode « Propose »).

Vérifie toi-même (compte de test créé puis supprimé) :
- l'onglet s'affiche bien sur ordinateur et sur mobile ;
- tableau_enregistrer refuse un format invalide ;
- avec de fausses données pour DEUX faux établissements (enregistrées puis effacées, liste d'établissements remise à l'état d'avant), chaque bloc s'affiche, le sélecteur et la vue d'ensemble fonctionnent, chaque bouton envoie la bonne mission avec le bon établissement, et tableau_enregistrer refuse un établissement hors liste ; avec un seul établissement, ni sélecteur ni vue d'ensemble ;
- si Activepieces n'est pas connecté, « Actualiser » donne un message clair de l'agent (« connectez Activepieces dans Connexions ») et pas une erreur.
Mets à jour PROJET.md.
```

## Premier test réel

Dans « Fiches Google », cliquer sur **Actualiser** (ou **Actualiser tout**). Puis, sur un avis, cliquer sur **Répondre** et vérifier qu'une carte « À valider » apparaît.

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 10, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 10 du dépôt {DEPOT} (étiquette etape-10) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
