#!/bin/bash

# notes :
#
#  - pour lancer le script :
#    - "./script.sh true" pour build
#    - "./script.sh" sinon
#
#  - pour investiguer : "docker compose logs -f"

GREEN='\e[32m'
NC='\e[0m' # Reset color

#### Gestion du premier argument
if [ "$1" == "true" ]; then
    BUILD_IMAGES=true
else
    BUILD_IMAGES=false
fi

#### Conf côté airflow
echo -e "AIRFLOW_UID=$(id -u)" >.env

#### Exécution de "docker compose down"

echo -e "${GREEN}\n\n== Exécution de \"docker compose down\" ${NC}"
docker compose down --remove-orphans

#### Exécution de "docker compose up airflow-init"

echo -e "${GREEN}\n\n== Exécution de \"docker compose up airflow-init\" ${NC}"

docker compose up airflow-init # doit se terminer par "airflow-init exited with code 0"
if [ $? -eq 0 ]; then
    echo "✅ Initialisation réussie."
else
    echo "❌ Échec de l'initialisation."
    exit 1
fi

#### Exécution de "docker compose up"

echo -e "${GREEN}\n\n== Exécution de \"docker compose up\" ${NC}"

if [ "$BUILD_IMAGES" = true ]; then
    docker compose up --build -d # si besoin de reconstruire l'image (si nouvelle lib dans le requirement.txt par exemple)
else
    docker compose up -d
fi

#### Attente jusqu'à ce que tous les conteneurs soient healthy

echo -e "${GREEN}\n\n== Attente jusqu'à ce que tous les conteneurs soient healthy ${NC}"

SECONDS_WAITED=0

while true; do
    UNHEALTHY=$(docker ps --filter "health=unhealthy" --format '{{.Names}}') # retourne les conteneurs "unhealthy"
    STARTING=$(docker ps --filter "health=starting" --format '{{.Names}}')   # retourne les conteneurs "starting"

    if [ -z "$UNHEALTHY" ] && [ -z "$STARTING" ]; then
        echo -e "${GREEN} Tous les conteneurs sont healthy.${NC}"
        break
    fi

    MINUTES=$((SECONDS_WAITED / 60))
    SECONDS=$((SECONDS_WAITED % 60))

    printf "\r+%dm%02ds : les conteneurs ne sont pas encore tous healthy..." "$MINUTES" "$SECONDS" # formatage des secondes sur 2 digits (\r pour réécrire la ligne)

    SECONDS_WAITED=$((SECONDS_WAITED + 5))
    sleep 5
done

# remarque lors de la migration airflow 2.11.0 vers 3.0.1 lors du lancement du script :
# "Network job_market_default Resource is still in use" (lié au déploiement précédent avec la 2.11.0)
# Il faut faire ce qui suit :
#   > docker network rm job_market_default
#       Error response from daemon: error while removing network: network job_market_default id dd473e2879f2f1dd1f58e86df954e9d67accce69bf2189323f0ff6adccf127f8 has active endpoints
#   > docker rm $(docker network inspect job_market_default -f '{{range .Containers}}{{.Name}} {{end}}')
#       Error response from daemon: cannot remove container "/flower": container is running: stop the container before removing or force remove
#       Error response from daemon: cannot remove container "/redis": container is running: stop the container before removing or force remove
#       Error response from daemon: cannot remove container "/postgres": container is running: stop the container before removing or force remove
#   > docker stop postgres redis flower
#   > docker network rm job_market_default
#       job_market_default
