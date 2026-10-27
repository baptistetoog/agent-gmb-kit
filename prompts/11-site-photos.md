# 11. Le site internet et les photos

**Ce qu'on voit à la fin :** dans Réglages, deux nouvelles sections.
- **Site internet :** on colle l'adresse du site, l'outil en relève toutes les pages, et l'agent met toujours le bon lien vers la bonne page dans ses posts.
- **Photos :** on dépose ses photos depuis l'ordinateur ou le téléphone. L'outil les héberge, l'agent les regarde, les décrit et choisit la bonne photo pour chaque post.

**Pourquoi pas Google Drive ?** Google ne publie une photo que si elle est accessible par une adresse publique. Une photo dans Drive devrait de toute façon être recopiée et hébergée quelque part. Le plus simple, et le moins technique, c'est de déposer les photos directement dans l'outil, depuis son téléphone.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Je veux que l'agent soit autonome pour les liens et les photos de ses posts.

1. LE SITE INTERNET (section « Site internet » dans l'onglet Réglages, admin ; avec design.css) :
   - Un champ « Adresse du site » et un bouton « Analyser le site ». Le champ est pré-rempli avec le site trouvé dans agent/ENTREPRISE.md, et si le site n'a encore jamais été analysé, l'analyse se lance toute seule au démarrage de l'outil : l'admin n'a rien à faire, sauf corriger l'adresse si elle est fausse.
   - Le serveur relève les pages : d'abord le sitemap (robots.txt puis /sitemap.xml ou /sitemap_index.xml, sitemaps imbriqués compris) ; à défaut, il suit les liens internes depuis l'accueil (même domaine, 200 pages au plus). Pour chaque page : adresse, titre, méta-description. Requêtes polies (une à la fois, délai court, 10 s maximum chacune, un user-agent clair). Seulement http/https sur le domaine indiqué, jamais d'adresse interne (127.0.0.1, réseau local).
   - Résultat : la liste des pages, regroupées par rubrique (établissements, offres ou services, zones/villes, tarifs, blog, contact…), et, s'il y a plusieurs établissements, le rattachement de chaque page à son établissement quand c'est clair (page du parc, de l'agence, du magasin…), affichée dans la section avec le nombre de pages et la date. Enregistré dans data/site/pages.json et recopié en lecture seule pour l'agent dans agent/site.md (une ligne par page : titre — adresse — en quelques mots).
   - Bouton « Actualiser », et actualisation automatique chaque lundi à 6 h.
   - Dans agent/CLAUDE.md, section « Le site » : chaque lien qu'il met (bouton d'un post, réponse, conseil) vient de site.md, et c'est la page la plus précise pour le sujet (la page de l'établissement, de la commune ou du service plutôt que l'accueil). Avec plusieurs établissements, un post ou une réponse d'un établissement ne renvoie jamais vers la page d'un autre. Il n'invente jamais une adresse. agent/site.md est interdit en écriture pour l'agent.
   - Dans les cartes « À valider », l'outil affiche un ⚠️ à côté de tout lien qui n'est pas dans la liste des pages du site.

2. LES PHOTOS (section « Photos » dans l'onglet Réglages ; ajout et suppression réservés aux admins) :
   - Dépôt par glisser-déposer ou bouton « Ajouter des photos » (plusieurs à la fois ; sur téléphone, cela ouvre l'appareil photo ou la galerie). JPEG, PNG ou WebP seulement, vérifiés par leur contenu (pas seulement l'extension), 10 Mo maximum chacune.
   - Le serveur enregistre chaque photo sous un nom aléatoire impossible à deviner (ex. 3f9c…e1.jpg) dans data/photos/, et la sert publiquement, sans connexion, à l'adresse https://{DOMAINE}/photos/<nom> : c'est indispensable pour que Google puisse la récupérer lors d'une publication. Aucune autre page de data/ n'est publique. Avant de rendre une photo publique, le serveur retire ses métadonnées (en particulier la position GPS), en gardant seulement l'orientation.
   - Un champ « Établissement » sur chaque photo (« Tous » par défaut ; s'il n'y a qu'un établissement, on ne l'affiche pas), qu'on choisit au dépôt et qu'on peut changer. Un filtre par établissement dans la galerie.
   - Une galerie en vignettes : pour chaque photo, sa description, ses mots-clés, son établissement, la date d'ajout, et « Utilisée le … dans le post … » si elle a servi ; boutons « Modifier la description » et « Supprimer ».
   - Après chaque ajout, l'agent regarde la photo et propose lui-même une description courte et des mots-clés (sujet, lieu si visible, service) : ajoute à app/mcp-plateforme.js l'outil photos_decrire(nom, description, mots_cles). L'agent voit les photos grâce à une copie en lecture seule dans agent/photos/ (il ne peut ni y écrire ni les supprimer).
   - Ajoute aussi photos_lister(etablissement facultatif) (nom, adresse publique, description, mots-clés, établissement, dernières utilisations) et photo_utilisee(nom, post) pour noter qu'une photo a servi.
   - Dans agent/CLAUDE.md, section « Les photos » : pour un post, il choisit une photo de la photothèque qui correspond au sujet, à l'établissement concerné (ou « Tous ») et qui n'a pas servi depuis au moins 4 semaines sur cette fiche ; il passe son adresse publique à create-post (champ mediaSourceUrl) ; il note l'utilisation (le serveur la note aussi lui-même quand un post validé est publié). La galerie signale les photos que Google risque de refuser (WebP, plus de 5 Mo, moins de 10 Ko ou moins de 250 px). S'il n'y a aucune photo adaptée, il le dit dans la carte et propose quelle photo prendre.
   - Dans les cartes « À valider » d'un post, la photo choisie s'affiche en vignette, et l'admin peut en choisir une autre avant de valider.

3. LE POST DE LA SEMAINE : mets à jour le modèle d'automatisation « Post de la semaine » (et l'automatisation existante si elle est déjà créée) : « Pour chaque établissement suivi, propose un post Google pour cette semaine avec le skill post-google, en variant le type par rapport à ses posts précédents, avec le lien de la page du site la plus adaptée et une photo de la photothèque, puis demande la validation pour le publier. » Mets aussi à jour le skill post-google avec ces règles de lien et de photo.

Vérifie toi-même (compte de test créé puis supprimé) :
- l'analyse du site de {ENTREPRISE} trouve ses pages (nombre, rubriques) et agent/site.md est rempli ;
- un dépôt de 2 photos de test (génère-les, par exemple une image unie avec un texte), refus d'un faux .jpg qui n'est pas une image, adresse publique accessible sans connexion, adresse d'un fichier de data/ refusée ;
- l'agent décrit une photo déposée ;
- demande à l'agent un post (sans le publier) : la carte « À valider » contient un lien du site (sans ⚠️) et une photo en vignette.
Ensuite, supprime les photos de test (garde l'analyse du site). Ne publie rien sur la vraie fiche Google. Mets à jour PROJET.md.
```

## À la main ensuite

- Réglages → Site internet : vérifier que l'adresse pré-remplie est la bonne (l'analyse se fait toute seule).
- Réglages → Photos : déposer 10 à 20 photos par établissement depuis son téléphone (lieu, équipe, clients en situation avec leur accord, produits, réalisations, avant/après…).

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 11, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 11 du dépôt {DEPOT} (étiquette etape-11) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
