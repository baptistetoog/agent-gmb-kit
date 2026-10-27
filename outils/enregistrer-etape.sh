#!/bin/bash
# À lancer depuis le dépôt de TRAVAIL du kit, après chaque prompt passé sur l'instance de test.
# Enregistre l'état de l'instance (code, fiche de l'agent, config système) après l'étape $1 ($2 = titre), sans données ni secrets.
#   outils/enregistrer-etape.sh 5 "Donner vie à l'agent"
set -e
cd "$(dirname "$0")/.."
UTIL=${UTIL:?Indiquez l'utilisateur Linux de l'instance de test : UTIL=montest outils/enregistrer-etape.sh 5 "Titre"}
NGINX=${NGINX:-$UTIL}           # le nom de son fichier nginx (sites-available)
N=$(printf "%02d" "$1")
rm -rf instance && mkdir -p instance/systeme
rsync -a --exclude 'node_modules' vps:/home/$UTIL/app instance/ 2>/dev/null || true
rsync -a --exclude 'work/' --exclude 'photos/' --exclude '.claude/settings.local.json' vps:/home/$UTIL/agent instance/ 2>/dev/null || true
rsync -a vps:/home/$UTIL/PROJET.md instance/ 2>/dev/null || true
ssh vps "cat /etc/systemd/system/$UTIL-app.service 2>/dev/null; for f in /etc/systemd/system/$UTIL-app.service.d/*.conf; do [ -f \"\$f\" ] && echo \"# \$f\" && cat \"\$f\"; done" > instance/systeme/agent-app.service 2>/dev/null || true
ssh vps "cat /etc/nginx/sites-available/$NGINX 2>/dev/null" > instance/systeme/nginx-agent.conf || true
# garde-fou : aucun secret dans le dépôt
if grep -rIl -E 'sk-ant-[a-z0-9]+-[A-Za-z0-9_-]{40,}|refresh_token"\s*:\s*"[^"]{8,}' instance >/dev/null 2>&1; then echo "SECRET DÉTECTÉ : rien n'est enregistré"; exit 1; fi
git add -A
git commit -q -m "Étape $N : $2" || echo "rien de nouveau"
git tag -f "etape-$N" >/dev/null
echo "Étape $N enregistrée ($(git rev-parse --short HEAD))"
