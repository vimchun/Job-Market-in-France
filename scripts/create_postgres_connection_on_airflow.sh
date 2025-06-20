#!/bin/bash

# Créer la connexion postgres pour pouvoir requêter la base de données "francetravail"
# doc : https://airflow.apache.org/docs/apache-airflow/2.0.1/howto/connection.html#creating-a-connection-from-the-cli

#### Configuration

CONTAINER_NAME="airflow-dag-processor"

CONN_ID="ma_connexion"
CONN_TYPE="postgres"
USERNAME="mhh"
PASSWORD="mhh"
HOST="postgres" # correspond au nom du conteneur postgres (voir docker-compose.yml)
PORT="5432"
DBNAME="francetravail"

#### Construction de l'URI Airflow
CONN_URI="${CONN_TYPE}://${USERNAME}:${PASSWORD}@${HOST}:${PORT}/${DBNAME}"

#### Exécution de la commande dans le conteneur
echo "Ajout de la connexion Airflow"

docker exec -it "$CONTAINER_NAME" \
    airflow connections add "$CONN_ID" --conn-uri "$CONN_URI"
