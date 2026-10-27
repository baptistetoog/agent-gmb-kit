# 4. Mettre l'outil en ligne sur son sous-domaine

## À la main : le sous-domaine (1 minute)

Chez le fournisseur du nom de domaine (GoDaddy, OVH, IONOS…), dans la zone DNS, ajouter :

| Type | Nom | Valeur | TTL |
|---|---|---|---|
| A | `agent` (la partie avant le domaine, ex. agent pour agent.monentreprise.fr) | l'adresse IP du VPS | 1 heure ou moins |

Puis créer son compte admin (le mot de passe est tapé par l'apprenant, il ne s'affiche pas) :

```bash
ssh -t vps 'sudo -iu {UTILISATEUR} node app/creer-compte.js {EMAIL_ADMIN} "Prénom Nom" admin'
```

## Puis ce prompt

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md pour comprendre le projet.

J'ai créé le sous-domaine {DOMAINE} qui pointe vers l'adresse IP du serveur. Mets l'outil en ligne :
1. Vérifie que {DOMAINE} pointe bien vers ce serveur (compare avec l'IP publique du serveur). Si ce n'est pas encore le cas, arrête-toi et dis-moi d'attendre.
2. Crée une configuration nginx dédiée, dans un nouveau fichier à son nom, qui envoie {DOMAINE} vers 127.0.0.1:{PORT}. Elle doit supporter le temps réel (Server-Sent Events : pas de mise en tampon, délai long), les envois de fichiers jusqu'à 20 Mo, et transmettre l'IP réelle du visiteur (X-Forwarded-For) pour le blocage des mots de passe.
3. Obtiens un certificat HTTPS Let's Encrypt avec certbot pour ce sous-domaine seulement, et redirige le HTTP vers le HTTPS.
4. Ajoute les en-têtes de sécurité habituels (HSTS, X-Content-Type-Options, Referrer-Policy, X-Frame-Options SAMEORIGIN).
5. Teste toujours la configuration avec `nginx -t` avant de recharger nginx, et ne modifie aucun autre site.
6. Si le serveur Node lit l'IP du visiteur, fais-lui utiliser X-Forwarded-For seulement quand la requête vient de 127.0.0.1.

Vérifie toi-même : https://{DOMAINE} répond avec un certificat valide et affiche la page de connexion. Mets à jour PROJET.md.
```

**Ce qu'on voit à la fin :** https://{DOMAINE} affiche la page de connexion, avec le cadenas.

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 4, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 4 du dépôt {DEPOT} (étiquette etape-04) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
