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

#### Exécution de "docker compose down"

echo -e "${GREEN}\n\n== Exécution de \"docker compose down\" ${NC}"
docker compose down

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
