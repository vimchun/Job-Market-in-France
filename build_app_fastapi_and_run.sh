# A lancer depuis le dossier "Job_Market"

docker build -f fastapi/Dockerfile -t app_fastapi .

# note :
# dans /fastapi, le fichier "requirements.txt" doit contenir les dépendances pour que fastapi tourne dans le conteneur

docker rm app_fastapi_container && docker run -d -p 8000:8000 --name app_fastapi_container app_fastapi

## pour investiguer si le conteneur ne se lance pas
# docker logs app_fastapi_container
