# 7. Les skills

**Ce qu'on voit à la fin :** une page « Skills » qui liste les savoir-faire de l'agent. On en crée un en deux clics, et l'agent l'applique tout seul quand la demande s'y prête. On peut aussi lui demander de transformer une méthode en skill.

---

```
Mon serveur est accessible par `ssh vps` (root). Lis d'abord /home/{UTILISATEUR}/PROJET.md. Tout ce que tu crées dans /home/{UTILISATEUR} doit appartenir à {UTILISATEUR}.

Ajoute les skills à l'agent. Un skill est une méthode écrite que l'agent applique quand la demande s'y prête. On utilise le format natif de Claude Code : un dossier agent/.claude/skills/<identifiant>/SKILL.md, avec en tête :
---
name: <identifiant>
description: <quand utiliser ce skill, en une ou deux phrases>
---
puis la méthode en Markdown.

1. Crée trois skills de départ. Ils doivent être OPÉRATIONNELS tout de suite : pas des modèles creux, mais des méthodes complètes, adaptées à l'entreprise. Lis d'abord agent/ENTREPRISE.md, agent/memoire.md et agent/regles.md, et appuie-toi sur les règles officielles de Google (recherche sur support.google.com : règles des contenus des fiches d'établissement, des posts et des avis), en citant la page source en bas de chaque skill.
   - reponse-avis : répondre à un avis Google.
     - Structure : remercier, reprendre un détail précis de l'avis (l'activité, le produit, le service, l'accueil, le délai…), une phrase sur l'entreprise ou l'établissement si utile, une conclusion. 40 à 80 mots pour un avis positif, un peu plus pour un avis négatif.
     - Cas par cas : 5 étoiles avec texte, 5 étoiles sans texte, 3-4 étoiles, 1-2 étoiles (reconnaître, ne jamais se justifier ni donner de détails privés en public, proposer un contact direct avec le téléphone de l'entreprise), avis suspect ou hors sujet (ne pas répondre sur le fond, proposer de le signaler, expliquer comment).
     - Ton et signature : ceux de ENTREPRISE.md et de la mémoire (la mémoire l'emporte). Si aucune signature n'est connue, signer « {SIGNATURE} ». Avec plusieurs établissements, la réponse parle de l'établissement concerné par l'avis (jamais d'un autre) et le téléphone proposé est le sien. Jamais deux fois la même formule d'ouverture : varier. Ne jamais recopier les exemples du skill : ils montrent le ton, pas le texte.
     - Interdits : promesses non tenables, données personnelles du client, mots-clés plaqués, copier-coller.
     - 6 exemples rédigés pour {ENTREPRISE} (un par cas, avec de vrais détails tirés de ENTREPRISE.md).
   - post-google : rédiger un post Google Business.
     - Types : nouveauté, offre (avec dates et conditions), événement (avec dates), conseil. Accroche dans les 80 premiers caractères (c'est ce qui s'affiche), 150 à 300 mots maximum (1 500 caractères), un seul bouton d'appel à l'action parmi ceux de Google (Réserver, Commander, Acheter, En savoir plus, S'inscrire, Appeler) avec le bon lien du site, une idée de photo précise.
     - Règles Google : pas de numéro de téléphone ni d'e-mail dans le texte (le bouton « Appeler » existe), pas de hashtags, pas de majuscules criardes, pas de contenu trompeur, pas de superlatif invérifiable (« le meilleur », « le seul »), pas de comparaison avec des concurrents. Si l'activité touche à un domaine réglementé (santé, produits chimiques, alcool, finance, enfants…), respecter ses règles de communication : jamais d'allégation interdite ou invérifiable (« sans danger », « non toxique », « garanti »…).
     - Un calendrier type sur 4 semaines adapté à l'activité et à la saison de {ENTREPRISE}, et 4 posts d'exemple prêts à publier. Avec plusieurs établissements : un post concerne UN établissement (lien vers sa page, ses dates, ses offres locales) ; une actualité commune à tout le réseau est déclinée établissement par établissement, sans texte identique d'une fiche à l'autre.
   - audit-fiche : auditer la fiche Google Business.
     - Check-list notée sur 100, par établissement : nom (exact, sans mot-clé ajouté : 10), catégorie principale et secondaires (15), description (750 caractères max, sans lien ni promo : 10), horaires y compris exceptionnels et cohérents avec le site (10), adresse ou zone desservie (10), services et produits (10), photos récentes (10), avis : volume, note et taux de réponse (15), posts dans les 30 derniers jours (5), questions/réponses (5).
     - Pour chaque point : état, note, correction prête à coller, priorité (haute / moyenne / basse).
     - Comparer avec ENTREPRISE.md (incohérences entre la fiche et le site = priorité haute).
     - Sortie : tableau de synthèse + 3 constats + 3 actions, enregistré dans agent/work/audit-gmb.md. Avec plusieurs établissements : un tableau par établissement, puis un classement des fiches de la moins complète à la plus complète.

2. Dans l'outil, ajoute une section « Skills » dans l'onglet « Réglages » du panneau (avec le système de design design.css) :
   - la liste des skills (nom + description) ;
   - un admin peut créer, modifier et supprimer un skill (nom, description, méthode), avec un aperçu ;
   - un membre peut seulement les lire ;
   - dans la zone de discussion, un petit bouton « / » permet de choisir un skill à appliquer au prochain message. Le message envoyé à l'agent se termine alors par « Applique le skill <identifiant>. » et l'interface montre une étiquette du skill sur la bulle.
   - côté serveur, l'identifiant est nettoyé (minuscules, chiffres, tirets) pour qu'on ne puisse pas écrire ailleurs que dans agent/.claude/skills/.

ATTENTION, point technique : Claude Code refuse toujours que l'agent écrive dans son dossier .claude/, même avec une autorisation. Pour qu'il puisse créer ses skills, ajoute un petit serveur MCP d'approbation app/mcp-approbation.js, passé à Claude avec --permission-prompt-tool : il répond « oui » uniquement pour écrire ou modifier agent/.claude/skills/<identifiant>/SKILL.md avec un en-tête valide, et « non » à tout le reste (les règles deny existantes passent avant lui). Ne passe jamais par le mode qui désactive toutes les vérifications. ATTENTION aussi : « --allowedTools Write » laisse l'agent écrire n'importe où sur le serveur. Retire Write et Edit de --allowedTools et lance Claude en mode --permission-mode acceptEdits : il écrit librement dans son dossier agent/, et toute écriture ailleurs passe par le serveur d'approbation, qui la refuse.

3. Dans agent/CLAUDE.md, ajoute une section « Tes skills » : il utilise ses skills quand la demande s'y prête. Quand on lui dit « fais-en un skill » ou qu'il remarque qu'il refait souvent la même méthode, il propose de créer un skill, et s'il a l'accord, il l'écrit lui-même dans .claude/skills/<identifiant>/SKILL.md au bon format.

Vérifie toi-même (compte de test créé puis supprimé) : invente un avis 2 étoiles réaliste pour {ENTREPRISE} (pour un établissement précis s'il y en a plusieurs), demande à l'agent d'y répondre, et vérifie dans le résultat brut de Claude qu'il a bien utilisé le skill reponse-avis (outil Skill) et respecté le ton de l'entreprise. Demande-lui aussi un post : il doit respecter les règles Google du skill (pas de téléphone, pas de hashtag). Puis demande-lui de créer un skill « demande-avis » (le message à envoyer à un client après {MOMENT_CLIENT} pour lui demander un avis Google, avec le lien d'avis du bon établissement) (signé comme les réponses aux avis : la mémoire, sinon « {SIGNATURE} ») et vérifie qu'il apparaît dans la section Skills : celui-là, on le garde. Pendant tes tests, ne publie rien et ne réponds à rien sur la vraie fiche Google, même si la connexion Activepieces existe. Mets à jour PROJET.md.
```

## Si ça ne marche pas

Décrivez d'abord ce que vous voyez à Claude (« J'ai collé le prompt 7, et je vois … au lieu de … ») : dans la plupart des cas, il corrige tout seul.

Si vous êtes vraiment bloqué, ce prompt remet votre outil exactement dans l'état de la fin de cette étape :

```
Mon serveur est accessible par `ssh vps` (root). Remets mon outil exactement à l'état de l'étape 7 du dépôt {DEPOT} (étiquette etape-07) : récupère le dossier instance/app de cette étiquette et remplace /home/{UTILISATEUR}/app par celui-ci, en faisant d'abord une sauvegarde. Ne touche ni à mes données (/home/{UTILISATEUR}/data), ni à ma clé Claude, ni aux fichiers de mon agent (/home/{UTILISATEUR}/agent). Remplace dans le code le domaine, l'utilisateur, le port et la charte de l'exemple par les miens ({DOMAINE}, {UTILISATEUR}, {PORT}, et la charte notée dans la section « Paramètres » de PROJET.md), redémarre le service et vérifie que la page de connexion répond. Si cette étiquette n'existe pas (encore) dans le dépôt, ne touche à rien et dis-le-moi.
```
