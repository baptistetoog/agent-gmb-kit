# 14. Option : parler à son agent

**Ce qu'on voit à la fin :** un bouton micro pour dicter son message, et un bouton pour que l'agent lise sa réponse à voix haute. Le tout dans le navigateur, sans service payant.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Ajoute la voix dans le bureau de l'agent, uniquement avec les fonctions du navigateur (aucun service payant, rien enregistré sur notre serveur ; à savoir : Chrome et Edge font la reconnaissance vocale chez Google ou Microsoft) :
1. Un bouton micro 🎤 à côté de la zone de saisie. Il utilise la reconnaissance vocale du navigateur (SpeechRecognition / webkitSpeechRecognition, langue fr-FR) : le texte s'écrit en direct dans la zone de saisie, on peut le corriger, puis on l'envoie. Le bouton change d'aspect pendant l'écoute. Si le navigateur ne le permet pas, le bouton est masqué.
2. Sur chaque réponse de l'agent, un petit bouton 🔊 qui lit la réponse à voix haute (speechSynthesis, voix française, sans lire les symboles Markdown). Un interrupteur « Lecture automatique » dans l'onglet Discussion lit chaque nouvelle réponse dès qu'elle est finie (réglage gardé dans le navigateur).
3. Pendant la lecture à voix haute, appelle bureau.parle(true) (sa bouche bouge dans la scène 3D), puis bureau.parle(false) à la fin.
4. Vérifie que l'en-tête Permissions-Policy (envoyé par nginx ou par le serveur Node) autorise le micro pour ce site (microphone=(self)), sans changer les autres sites.
5. Dans agent/regles.md, ajoute : « Les messages peuvent être dictés à la voix : comprends l'intention malgré les fautes de transcription. »

Vérifie que rien n'a cassé (la page se charge, aucune erreur dans la console) et mets à jour PROJET.md.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 14, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 14 du dépôt {DEPOT} (étiquette etape-14) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
