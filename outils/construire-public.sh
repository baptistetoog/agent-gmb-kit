#!/bin/bash
# Construit le dépôt PUBLIC du kit à partir du dépôt de travail : pour chaque étiquette etape-NN,
# ne garde que le code (instance/app, instance/systeme), le kit et les prompts génériques,
# remplace les valeurs de l'instance de test par celles de l'exemple, et vérifie qu'il ne reste ni donnée client ni secret.
# Les valeurs de l'instance de test sont dans outils/instance-test.json (jamais publié, voir instance-test.exemple.json).
set -e
cd "$(dirname "$0")/.."
SRC=$(pwd)
PUB="$SRC/../agent-gmb-kit-public"
CONF="$SRC/outils/instance-test.json"
[ -f "$CONF" ] || { echo "Créez d'abord outils/instance-test.json (copie de instance-test.exemple.json)"; exit 1; }
REMPLACEMENTS=$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))["remplacements"]))' "$CONF")
INTERDIT=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["interdit"])' "$CONF")'|sk-ant-[a-z0-9]+-[A-Za-z0-9_-]{40,}'

rm -rf "$PUB" && mkdir -p "$PUB" && cd "$PUB" && git init -q -b main
for TAG in $(git -C "$SRC" tag | sort); do
  find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  git -C "$SRC" archive "$TAG" | tar -x
  rm -rf instance/agent instance/PROJET.md mes-prompts outils/instance-test.json .gitignore
  REMPLACEMENTS="$REMPLACEMENTS" python3 - <<'PY'
import json, os
R = json.loads(os.environ["REMPLACEMENTS"])
for base, _, fichiers in os.walk("."):
    if ".git" in base: continue
    for f in fichiers:
        p = os.path.join(base, f)
        try: s = open(p, encoding="utf-8").read()
        except Exception: continue
        t = s
        for a, b in R: t = t.replace(a, b)
        if t != s: open(p, "w", encoding="utf-8").write(t)
PY
  if grep -rIl -i -E "$INTERDIT" . --exclude-dir=.git; then
    echo "DONNÉE INTERDITE TROUVÉE dans $TAG : arrêt"; exit 1
  fi
  git add -A && git commit -q -m "$(git -C "$SRC" log -1 --format=%s "$TAG")" --allow-empty && git tag "$TAG"
  echo "$TAG ok"
done
git log --oneline | head -20
