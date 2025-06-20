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

echo -e "AIRFLOW_UID=$(id -u)" >.env # Le fichier .env est nécéssaire dans ce cas

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

# Notes investigation en vrac :

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

# Nettoyage réseau si nécessaire (optionnel)
#NETWORK_NAME="job_market_default"
#if docker network inspect "$NETWORK_NAME" &>/dev/null; then
#    echo -e "${GREEN}\n\n== Nettoyage du réseau $NETWORK_NAME si possible ${NC}"
#    docker network rm "$NETWORK_NAME" 2>/dev/null || echo "ℹ️  Réseau $NETWORK_NAME non supprimé (encore utilisé ?)"
#fi

# remarque lors du rollback airflow 3.0.1 vers 2.11.0 lors du lancement du script :
# Error response from daemon: Conflict. The container name "/flower" is already in use by container "3a0b903e99c2667f9e5e4456429115519926ef3e34755aac3a77e416d72ec08f". You have to remove (or rename) that container to be able to reuse that name.
# => docker rm -f flower

# installation avec 2.11.0 :
# > docker ps
# CONTAINER ID   IMAGE                           COMMAND                  CREATED         STATUS                   PORTS                              NAMES
# 21864f919b81   airflow2110-airflow-worker      "/usr/bin/dumb-init …"   5 minutes ago   Up 5 minutes (healthy)   8080/tcp                           airflow-worker
# 30de0af49c23   airflow2110-flower              "/usr/bin/dumb-init …"   5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:5555->5555/tcp, 8080/tcp   flower
# 1d455b985939   airflow2110-airflow-scheduler   "/usr/bin/dumb-init …"   5 minutes ago   Up 5 minutes (healthy)   8080/tcp                           airflow-scheduler
# 56d5f0e009b7   airflow2110-airflow-webserver   "/usr/bin/dumb-init …"   5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:8080->8080/tcp             airflow-webserver
# 9cf3c5e5e45d   airflow2110-fastapi             "uvicorn main:app --…"   5 minutes ago   Up 5 minutes             0.0.0.0:8000->8000/tcp             fastapi
# f5679f27015a   postgres:16-alpine              "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   0.0.0.0:5432->5432/tcp             postgres
# 16bdc2dd31d1   redis:latest                    "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   0.0.0.0:6379->6379/tcp             redis

# migration vers 3.1.0 :
# peut être utile de supprimer les logs dans airflow/logs
# > docker compose -f docker-compose--airflow-3-0-1.yml up airflow-init
# => supprimer les services qui empêchent l'exécution de cette commande

# check si erreur au setup de la 3.1.0 :
# docker exec -it airflow-init_3_0_1 bash
# root@b73a5fd4c85a:/opt/airflow# airflow db check
#   => doit répondre "INFO - Connection successful"

# Parfois (3.1.0), le service worker ne se lance pas, du coup, on accès à la gui mais les tâches ne se lancent pas...
