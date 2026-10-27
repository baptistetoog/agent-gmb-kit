# 13. L'agent ajoute des fonctionnalités à son outil

**Ce qu'on voit à la fin :** on demande à l'agent « ajoute un bouton qui… ». Il code la fonctionnalité sur une copie de l'outil et montre les changements. On clique sur « Appliquer » et l'outil se met à jour. En cas de problème, un retour arrière se fait tout seul ou en un clic.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Je veux que l'agent puisse améliorer son propre outil (ajouter un bouton, une page, un tableau…), mais sans jamais casser l'outil en ligne. Crée « l'atelier ».

1. LA DEMANDE : dans app/mcp-plateforme.js, ajoute l'outil proposer_fonctionnalite(titre, description_detaillee). Il crée une carte « Fonctionnalité » dans les validations, avec un bouton « Lancer la fabrication » (admin).
   Dans agent/CLAUDE.md, section « Ton atelier » : quand on lui demande une amélioration de l'outil, ou qu'il en voit une utile, il la décrit précisément (ce qu'on voit, où, comment ça marche) avec proposer_fonctionnalite. Il ne touche jamais lui-même au code de l'outil en ligne. Ajoute aussi à ses règles deny les dossiers atelier/ et sauvegardes/.

2. LA FABRICATION (au clic sur « Lancer la fabrication ») :
   - Le serveur copie app/ dans /home/{UTILISATEUR}/atelier/<n°>/app (sans data/).
   - Il lance Claude dans ce dossier (modèle sonnet, Read/Write/Edit/Glob/Grep, toujours sans Bash) avec la description, PROJET.md en lecture, et la consigne : faire le changement le plus simple et le plus propre, sans dépendance npm, sans toucher à la connexion, aux comptes ni aux secrets.
   - Ensuite, le serveur vérifie lui-même : `node --check` sur chaque fichier .js modifié, et démarrage d'essai de la copie sur un port libre (avec un dossier data/ vide temporaire) qui doit répondre sur la page de connexion en moins de 10 secondes.
   - La carte affiche le résumé de l'agent, la liste des fichiers modifiés et le diff (lisible, en couleurs), plus le résultat des vérifications. Bouton « Appliquer » (seulement si les vérifications sont passées) ou « Abandonner ».

3. L'APPLICATION (au clic sur « Appliquer ») :
   - sauvegarde complète de app/ dans /home/{UTILISATEUR}/sauvegardes/app-<date-heure>/ (on garde les 10 dernières) ;
   - copie des fichiers modifiés dans app/ ;
   - redémarrage de l'outil : le serveur répond d'abord à la page, puis s'arrête proprement, et systemd le relance.

4. LE FILET DE SÉCURITÉ :
   - Le service ne lance plus server.js directement mais un petit lanceur, app/lanceur.js (qui, lui, n'est jamais modifié par l'atelier). Il démarre server.js ; si une application vient d'avoir lieu (fichier marqueur dans data/) et que le serveur plante ou ne répond pas sur 127.0.0.1:{PORT} dans les 20 secondes, il restaure automatiquement la dernière sauvegarde, relance et note l'incident dans les validations.
   - Une section « Historique des versions » dans l'onglet « Réglages » (admin) liste les sauvegardes, avec un bouton « Revenir à cette version ».
   - L'atelier refuse de modifier app/lanceur.js, app/atelier.js (son propre filet), app/creer-compte.js et app/public/bureau3d.js (la scène fournie avec le kit). Le Claude de l'atelier n'a accès qu'à son dossier de copie : ni data/, ni la clé Claude, ni /proc (mêmes règles deny que l'agent, dans un .claude/settings.json créé dans la copie).

Vérifie toi-même (compte de test créé puis supprimé) : demande à l'agent d'ajouter dans le bureau un compteur « Messages échangés aujourd'hui ». Lance la fabrication, contrôle le diff, applique, et vérifie que l'outil redémarre avec le compteur. Puis teste le filet : applique à la main une version volontairement cassée par le même chemin (marqueur + fichier cassé) et vérifie que le lanceur revient seul à la version précédente. Enfin, garde ou retire le compteur selon ce qui est le plus propre, et dis-moi ce que tu as fait. Mets à jour PROJET.md.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 13, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 13 du dépôt {DEPOT} (étiquette etape-13) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
