#!/bin/bash

RED='\e[31m'
NC='\e[0m' # Reset color

#### Exécution de "docker compose up airflow-init"

echo -e "${RED}== Exécution de \"docker compose up airflow-init\" ${NC}"

docker compose up airflow-init  # doit se terminer par "airflow-init exited with code 0"
if [ $? -eq 0 ]; then
    echo "✅ Initialisation réussie."
else
    echo "❌ Échec de l'initialisation."
    exit 1
fi

#### Exécution de "docker compose up"

echo -e "${RED}== Exécution de \"docker compose up\" ${NC}"
docker compose up
