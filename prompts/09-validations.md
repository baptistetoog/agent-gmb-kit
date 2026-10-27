# 9. « Propose » ou « agit seul » : les validations

**Ce qu'on voit à la fin :** par défaut, l'agent lit librement mais ne publie rien sans accord. Ses actions arrivent sous forme de cartes « À valider ». Un clic sur « Valider » et c'est l'agent qui exécute. Un interrupteur permet de le laisser agir seul.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Je veux garder la main sur ce que l'agent fait dans le monde réel (répondre à un avis, publier un post, modifier la fiche Google).

1. LE MODE DE L'AGENT : un réglage enregistré dans data/reglages.json, modifiable par un admin depuis le bureau (interrupteur bien visible, sous le personnage) :
   - « Propose » (par défaut) : il lit et prépare, mais toute action qui modifie quelque chose passe par une validation ;
   - « Agit seul » : il peut tout faire directement.

2. LE TRI DES OUTILS : dans la section Connexions des Réglages, après « Tester », chaque outil de la connexion apparaît avec une case « Action (à valider) ». On la pré-coche automatiquement si le nom ou la description de l'outil parle d'écrire (create, update, delete, reply, post, publish, send, add, remove, patch, upload…). Les outils de lecture (get, list, search, find, read…) restent libres. L'admin peut corriger. Pour le type « API avec clé », l'outil appel_api est une action dès que l'écriture est autorisée. Ajoute alors à app/mcp-api.js un second outil lire_api (GET seulement), toujours libre, pour que l'agent puisse encore lire l'API en mode « Propose ». Le tri est enregistré par connexion.

   Pour ap_run_action d'Activepieces, le tri se fait ACTION PAR ACTION, pas par outil : en mode « Propose », ap_run_action n'est ni autorisé ni interdit d'avance, et le serveur MCP d'approbation (celui de l'étape des skills, passé avec --permission-prompt-tool) décide selon actionName : lecture libre (list-accounts, list-locations, get-location, list-reviews, get-review, list-posts, get-post, list-media, get-media, et custom_api_call en GET), écriture refusée avec le message « utilise d'abord demander_validation » (create-post, update-post, delete-post, reply-to-review, create-reply, delete-review-reply, update-location, custom_api_call hors GET). Une pièce autre que google-my-business est refusée.

3. LA DEMANDE DE VALIDATION : un petit serveur MCP stdio intégré, app/mcp-plateforme.js, toujours branché, avec l'outil demander_validation(titre, ce_que_je_vais_faire, outil_prevu, contenu_exact). Il crée une carte dans data/validations.json (statut « en attente ») et répond à l'agent : « Demande n°X envoyée, attends la réponse. »
   En mode « Propose », le serveur ajoute à --disallowedTools tous les outils marqués « Action ». Dans agent/CLAUDE.md, section « Tes validations » (elle remplace toute règle plus ancienne du type « ne rien publier sans accord ») : s'il a besoin d'une action, il prépare tout, appelle demander_validation avec le contenu exact (le texte de la réponse à l'avis, du post, etc.), puis il s'arrête.

4. LES CARTES « À VALIDER » dans un onglet « À valider » du panneau (pastille avec le nombre sur l'onglet, visibles par les admins ; dans la scène 3D, appelle bureau.statut("alerte") quand une carte attend : un panneau « ! » apparaît au-dessus du bureau) : titre, ce que l'agent va faire, le contenu exact (que l'admin peut corriger avant de valider), et les boutons « Valider » et « Refuser » (avec un motif facultatif).
   - Valider : le serveur relance l'agent dans la même discussion, avec les outils d'action autorisés pour CE lancement seulement, et le message : « Validation n°X accordée par <prénom>. Exécute exactement cette action, rien d'autre : <contenu final>. Puis confirme en une phrase. » La carte passe à « exécutée » avec le résultat.
   - Refuser : la carte passe à « refusée ». L'agent reçoit le motif dans la discussion et le retient dans sa mémoire s'il est utile pour la suite.
   - Tout est historisé (qui, quand, quoi).

Vérifie toi-même (compte de test créé puis supprimé) : avec une connexion « API avec clé » de test vers une API publique, écriture autorisée, en mode « Propose », demande à l'agent de faire un POST. Il doit créer une demande de validation, sans faire l'appel. Valide-la par l'API et vérifie qu'il la relance et l'exécute (une erreur de l'API de test est acceptable : c'est la tentative qui compte). Puis supprime la connexion et les cartes de test. Mets à jour PROJET.md.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 9, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 9 du dépôt {DEPOT} (étiquette etape-09) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
