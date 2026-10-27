# 12. Les automatisations

**Quand :** après le tableau de bord. L'agent sait alors lire la fiche, répondre aux avis et publier, et chaque action passe par une validation. Automatiser, c'est simplement lui confier ces mêmes missions à heure fixe.

**Comment :** on ne choisit pas les automatisations à la place de l'entreprise. Au premier lancement, l'agent mène un court entretien : il demande ce que l'entreprise veut automatiser, à quel rythme, et s'il doit proposer ou agir seul. Il propose ensuite chaque automatisation sous forme de carte « Activer ». On peut aussi lui dire à tout moment « automatise ça ».

**Ce qu'on voit à la fin :** une page « Automatisations » avec des tâches programmées, par exemple « Nouveaux avis » chaque matin, « Post de la semaine » le lundi et « Bilan du mois » le 1er. Chacune a un interrupteur, un bouton « Lancer maintenant » et le résultat de son dernier passage. Avec plusieurs établissements, chaque automatisation passe sur tous les établissements suivis, ou seulement ceux qu'on coche.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Ajoute les automatisations : des missions que l'agent fait tout seul à heure fixe. Reste simple.

1. LA SECTION « AUTOMATISATIONS » dans l'onglet « Réglages » (avec le système de design design.css ; création et modification réservées aux admins, lecture pour tous) :
   - chaque automatisation a : un nom, la consigne donnée à l'agent (la mission), une fréquence (tous les jours / chaque semaine tel jour / chaque mois tel jour du mois) et une heure (fuseau Europe/Paris), un interrupteur actif / en pause, la date du dernier passage et son résultat en une ligne ;
   - boutons « Lancer maintenant », « Modifier », « Supprimer » ;
   - trois modèles prêts à ajouter en un clic (ajoutés en pause) :
     - « Nouveaux avis », tous les jours à 9 h : « Actualise les avis de chaque établissement suivi. Pour chaque nouvel avis sans réponse, rédige une réponse avec le skill reponse-avis et demande la validation pour la publier. S'il n'y a rien de nouveau, dis-le en une phrase. »
     - « Post de la semaine », le lundi à 9 h : « Pour chaque établissement suivi, propose un post Google pour cette semaine avec le skill post-google, en variant le type par rapport à ses posts précédents, avec le lien de la page du site la plus adaptée et une photo de la photothèque, puis demande la validation pour le publier. »
     - « Bilan du mois », le 1er du mois à 9 h : « Fais l'audit de chaque fiche suivie avec le skill audit-fiche, mets à jour le tableau de bord et résume en 3 constats et 3 actions (avec plusieurs établissements : d'abord le classement des fiches, puis les 3 actions prioritaires pour le réseau). »
   - Une automatisation peut viser tous les établissements (par défaut) ou une partie d'entre eux : champ « Établissements » (cases à cocher, masqué s'il n'y en a qu'un), rappelé au début de la consigne envoyée à l'agent.
   - Tout est enregistré dans data/automatisations.json.

2. LE PLANIFICATEUR (dans le serveur) : toutes les minutes, il regarde les automatisations actives arrivées à échéance et les met dans la file de l'agent, comme un message normal, mais signé « Automatisation : <nom> ». Il ne rattrape pas les passages manqués pendant un arrêt. Une automatisation ne peut pas être lancée deux fois en même temps. Le résultat (la dernière réponse de l'agent, en une ligne) est enregistré dans l'automatisation. Si l'agent a créé des cartes « À valider », la pastille de l'onglet « À valider » et le « ! » de la scène les montrent comme d'habitude. Le voyant « Prochaine automatisation » de « État du système » s'active et affiche la prochaine échéance (nom + jour + heure).
   Chaque automatisation tourne dans sa propre discussion (pas dans la discussion principale), mais on voit son passage dans la discussion principale sous forme d'une ligne discrète : « 🕘 Nouveaux avis : 2 réponses à valider (Lyon, Nantes) ».

3. L'ENTRETIEN DE DÉMARRAGE :
   - Ajoute à app/mcp-plateforme.js l'outil proposer_automatisation(nom, consigne, frequence, jour, heure). Il crée une carte « Automatisation » dans les validations, avec un bouton « Activer » (admin). Au clic, l'automatisation est créée et activée.
   - Dans agent/CLAUDE.md, section « Tes automatisations » : tant qu'aucune automatisation n'existe (la page de l'outil le lui indique en ajoutant au premier message de chaque discussion la ligne « [Automatisations actives : aucune] » ou la liste), il propose, au début d'une discussion, un court entretien de 3 questions maximum, une à la fois :
     1) Qu'est-ce que vous aimeriez que je fasse tout seul sur vos fiches Google (répondre aux avis, publier, surveiller la fiche) ? Avec plusieurs établissements : pour tous, ou seulement certains ?
     2) À quel rythme ?
     3) Je vous propose tout avant de publier, ou je peux agir seul sur certaines choses ?
     Puis il propose chaque automatisation avec proposer_automatisation, et note les choix dans sa mémoire. Plus tard, si on lui dit « automatise ça » ou s'il remarque qu'on lui demande souvent la même chose, il propose une automatisation de la même façon.
   - La réponse à la question 3 règle le mode de l'agent (« Propose » ou « Agit seul »). L'agent ne peut pas le changer lui-même : il le recommande dans la carte, et c'est l'admin qui l'applique avec l'interrupteur.

Vérifie toi-même (compte de test créé puis supprimé) : ajoute le modèle « Nouveaux avis », règle-le pour passer dans 2 minutes et vérifie que le planificateur le lance, qu'il tourne dans sa propre discussion, et que le résultat s'enregistre (si Activepieces n'est pas connecté, un message clair de l'agent suffit). Teste « Lancer maintenant ». Lance une nouvelle discussion et vérifie que l'agent propose l'entretien, puis que proposer_automatisation crée bien une carte « Activer » qui fonctionne. Remets ensuite tout à zéro (aucune automatisation, aucune carte de test). Mets à jour PROJET.md.
```

## Premier test réel

Ouvrir une nouvelle discussion et répondre aux 3 questions de l'agent. Cliquer sur **Activer** sur les cartes qu'il propose. Le lendemain à 9 h, vérifier les réponses aux avis dans « À valider ».

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 12, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 12 du dépôt {DEPOT} (étiquette etape-12) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
