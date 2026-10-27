# 8. Les connexions : API et MCP (Activepieces)

**Ce qu'on voit à la fin :** une page « Connexions ». On ajoute Activepieces en collant son adresse MCP, on clique sur « Connecter », on se connecte à Activepieces, et l'agent peut lire la fiche Google. On peut aussi brancher n'importe quel outil qui fournit une clé API.

## À préparer à la main dans Activepieces

1. Créer un compte sur cloud.activepieces.com (gratuit pour commencer).
2. Dans le projet, aller dans **Connexions**, puis **Nouvelle connexion** → **Google My Business**, et se connecter avec le compte Google qui gère la ou les fiches (bouton « Se connecter avec Google »). Pour un réseau, prendre de préférence le compte qui a accès à toutes les fiches du périmètre (propriétaire ou gestionnaire du groupe d'établissements) ; si les fiches sont réparties sur plusieurs comptes Google, créer une connexion par compte.
3. C'est tout : l'outil se connecte ensuite à Activepieces tout seul, en un clic, et retrouve cette connexion Google.

## Puis ce prompt

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Ajoute une section « Connexions » dans l'onglet « Réglages » (réservée aux admins, avec le système de design design.css) pour brancher des outils externes à l'agent. Il y a deux types de connexion.

MISE EN ROUTE : l'étape 2 de la carte « Mise en route » devient active. Elle affiche un gros bouton « Connecter ma fiche Google » qui crée directement la connexion « activepieces » (adresse https://cloud.activepieces.com/mcp pré-remplie) et ouvre la page de connexion Activepieces. Au retour, l'étape se coche, et le voyant « Google / Activepieces » de « État du système » passe au vert (connexion testée comme expliqué dans « Cas particulier Activepieces » plus bas ; s'il n'y a aucune connexion Google My Business active, on affiche « Ajoutez une connexion Google My Business dans votre projet Activepieces »).

TYPE 1 — « Serveur MCP (connexion OAuth) », par exemple Activepieces (https://cloud.activepieces.com/mcp) :
- L'admin donne un nom (ex. activepieces) et l'adresse du serveur MCP, puis clique sur « Connecter ».
- Le serveur suit la norme MCP d'autorisation : découverte (/.well-known/oauth-protected-resource, sinon /.well-known/oauth-authorization-server sur l'origine), enregistrement automatique du client (Dynamic Client Registration) avec l'adresse de retour https://{DOMAINE}/api/oauth/retour, puis autorisation avec PKCE (S256), le paramètre resource et un state à usage unique lié à la session de l'admin.
- Au retour, le serveur échange le code contre les jetons, les enregistre dans data/oauth/<nom>.json (droits 600) et affiche « Connecté ». Les jetons ne sont jamais renvoyés au navigateur.
- L'agent parle à ce serveur grâce à un petit pont app/mcp-pont.js (stdio ↔ « Streamable HTTP », sans dépendance). Il ajoute le jeton, le renouvelle tout seul avec le refresh_token quand il expire ou sur une erreur 401, garde l'en-tête mcp-session-id, gère les réponses JSON et text/event-stream, et masque les jetons dans tous les messages d'erreur. Si la connexion a expiré, l'erreur dit à l'agent : « un admin doit reconnecter <nom> dans Connexions ».

TYPE 2 — « API avec clé » :
- L'admin donne un nom, l'URL de base de l'API, le nom de l'en-tête (ex. Authorization ou X-API-Key), un préfixe facultatif (ex. « Bearer ») et la clé. Une case « Autoriser l'écriture » est décochée par défaut.
- La clé est enregistrée dans data/connexions.json (droits 600) et n'est plus jamais affichée en entier (seulement les 4 derniers caractères).
- L'agent y accède par un petit serveur MCP stdio app/mcp-api.js avec un seul outil, appel_api(methode, chemin, corps). Il n'autorise que les chemins sous l'URL de base, n'accepte que GET si l'écriture n'est pas autorisée, ajoute la clé lui-même, coupe les réponses trop longues (50 000 caractères) et masque la clé si elle apparaît.

CAS PARTICULIER ACTIVEPIECES (important) : son serveur MCP ne fournit pas d'outils Google dédiés, mais une quarantaine d'outils génériques ap_*. Les actions Google passent toutes par ap_run_action(pieceName, actionName, input, connectionExternalId), avec pieceName « @activepieces/piece-google-my-business ». Donc :
- le test de la connexion appelle aussi ap_list_connections et compte les connexions ACTIVE de la pièce google-my-business (c'est ce nombre qui fait passer le voyant au vert, pas le nom des outils) ;
- les outils d'aide en lecture (ap_list_connections, ap_research_pieces, ap_search_actions, ap_get_piece_props, ap_resolve_property_options, ap_resolve_property_chain, ap_setup_guide) sont libres ;
- tous les autres outils ap_* (création de flows, tables, suppression…) sont toujours interdits à l'agent : il n'a pas à construire d'automatisations chez Activepieces ;
- ap_run_action sera trié action par action à l'étape des validations.

Pour chaque connexion, la page montre : le statut (connecté / à reconnecter / erreur), un bouton « Tester » (il lance le pont, fait initialize puis tools/list et affiche la liste des outils disponibles), « Reconnecter » et « Supprimer ».

Branchement à l'agent : à chaque lancement de Claude, le serveur génère un fichier de configuration MCP temporaire (dans data/, droits 600, supprimé après) avec toutes les connexions actives, et le passe avec --mcp-config et --strict-mcp-config. Ajoute « mcp__<nom>__* » de chaque connexion aux outils autorisés (sauf les exceptions d'Activepieces ci-dessus). Les secrets ne passent que par des variables d'environnement ou des fichiers que l'agent ne peut pas lire (data/ est déjà interdit à l'agent).

Dans agent/CLAUDE.md, ajoute une section « Tes connexions » : il regarde quels outils il a (mcp__…) avant de dire qu'il ne peut pas faire quelque chose. Il préfère les données réelles des fiches via Activepieces à toute supposition. S'il y a plusieurs connexions Google My Business, il utilise celle qui gère l'établissement concerné. Si une connexion est en erreur, il le dit simplement. En attendant l'étape des validations, il ne publie, ne modifie et ne répond à rien sur la fiche sans l'accord explicite de la personne : il propose d'abord le texte.

Vérifie toi-même :
- la découverte OAuth de https://cloud.activepieces.com/mcp fonctionne (affiche les adresses trouvées et le client_id obtenu par l'enregistrement, mais pas de secret) et le lien d'autorisation est bien formé ;
- ajoute une connexion « API avec clé » de test vers une API publique qui n'a pas besoin de vraie clé (par exemple https://api.github.com avec une fausse clé dans un en-tête X-Test), teste-la avec un GET via le pont, vérifie qu'un POST est refusé et que la fausse clé n'apparaît dans aucune réponse ; puis supprime-la ;
- l'agent voit bien l'outil appel_api quand la connexion existe.
Je ferai moi-même le clic sur « Connecter » pour Activepieces. Mets à jour PROJET.md.
```

## À la main ensuite

Dans l'outil : Connexions → Activepieces → **Connecter**, puis se connecter à Activepieces et accepter. Enfin **Tester** : la liste des outils Google My Business doit apparaître.

Premier test avec l'agent : « Fais l'audit de notre fiche Google à partir des vraies données. »

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 8, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 8 du dépôt {DEPOT} (étiquette etape-08) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
