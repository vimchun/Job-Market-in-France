# note :
#  - contexte = dossier "Job_Market" dans le fichier "docker-compose.yml"

FROM python:3.12-slim

# Définir le workir "/app" dans le conteneur
WORKDIR /app

# Copier le script "main.py" dans "/app"
COPY fastapi/main.py  .

# Ecraser le chemin du fichier csv
ENV LOCATION_CSV_PATH=/app/code_name__city_department_region.csv

# Copier le "requirements.txt" dans "/app"
COPY fastapi/requirements.txt  .

# Installer les dépendances
RUN pip install  --no-cache-dir  -r requirements.txt

# Exposer le port sur lequel l'application va tourner (par défaut, FastAPI utilise 8000)
EXPOSE 8000

# Lancer fastapi avec Uvicorn <=> "uvicorn main:app --host 0.0.0.0 --port 8000" ("--reload" pour le dev, à éviter en prod)
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  # prod
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
