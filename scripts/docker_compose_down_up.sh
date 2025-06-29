#!/bin/bash

# Script d'automatisation Docker pour Airflow
#
# Exécute les commandes suivantes :
#  - docker compose down
#  - docker compose up airflow-init
#  - docker compose up
#
#
# Accepte 2 paramètres :
#
#   - $1 : supprimer les volumes (true|false) lors du "docker compose down"
#          (false par défaut)
#          ⚠️ efface les données dont la base 'francetravail'
#
#   - $2 : rebuild de l'image apache/airflow:3.0.x défini dans le Dockerfile (true|false) lors du "docker compose up"
#          (false par défaut)
#
#
# Exemple d'exécution :
#   ./scripts/docker_compose_down_up.sh true true

#### Pour la coloration des prints

GREEN='\e[32m'
RED='\e[31m'
YELLOW='\e[33m'
BLUE='\e[34m'
MAGENTA='\e[35m'
CYAN='\e[36m'
WHITE='\e[37m'
NC='\e[0m' # Reset color

#### Variables
COMPOSE_FILE="docker-compose.yml"

#### Les 2 paramètres avec une valeur par défaut

REMOVE_VOLUMES=${1:-false} # attention, ça supprime les données, dont la db francetravail
BUILD_IMAGES=${2:-false}

echo -e "${GREEN}\n\n== Print des variables et paramètres ${NC}"

echo -e "${MAGENTA}"
echo -e "COMPOSE_FILE = ${COMPOSE_FILE}"
echo -e "[param 1] REMOVE_VOLUMES = ${REMOVE_VOLUMES}"
echo -e "[param 2] BUILD_IMAGES = ${BUILD_IMAGES}"
echo -e "${NC}"

#### Exécution de "docker compose down"
echo -e "${GREEN}\n\n== Exécution de \"docker compose down\" ${NC}"

#### pas besoin si on ne travaille que sur une version ? (à vérifier pour les prochaines versions d'airflow)
## echo "Arrêt et suppression de tous les conteneurs en exécution ou pas :"
## # on arrête puis supprime tous les conteneurs en exécution et en arrêt pour que la future
## #  commande "docker compose up airflow-init" s'exécute sans problème
## docker ps -aq | xargs -r docker stop
## docker ps -aq | xargs -r docker rm

if [ "$REMOVE_VOLUMES" = true ]; then
    echo "docker compose down avec remove volume"
    docker compose -f "$COMPOSE_FILE" down --remove-orphans -v --rmi all
else
    echo "docker compose down sans remove volume"
    docker compose -f "$COMPOSE_FILE" down --remove-orphans --rmi all
fi
# "-v" car la réinitialisation de la db Airflow peut permettre d'éviter certains pbs au setup
# "--rmi all" pour supprimer toutes les images utilisées par les services du fichier docker-compose.yml

#### Exécution de "docker compose up airflow-init"

echo -e "${GREEN}\n\n== Exécution de \"docker compose up airflow-init\" ${NC}"

docker compose -f "$COMPOSE_FILE" up airflow-init
if [ $? -eq 0 ]; then # doit se terminer par "airflow-init exited with code 0"
    echo "Initialisation réussie"
else
    echo "Échec de l'initialisation"
    exit 1
fi

#### Exécution de "docker compose up"

echo -e "${GREEN}\n\n== Exécution de \"docker compose up\" ${NC}"

if [ "$BUILD_IMAGES" = true ]; then
    docker compose -f "$COMPOSE_FILE" up --build -d # si besoin de reconstruire l'image (si nouvelle lib dans le requirement.txt par exemple)
else
    docker compose -f "$COMPOSE_FILE" up -d
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
