FROM python:3.12-slim

# Définir le workir "/app" dans le conteneur
WORKDIR /app

# Copier le script fastapi dans le workdir
COPY fastapi/main.py  .

# Copier le "code_name__city_department_region.csv" dans "/app/locations_information"
COPY api_extract__transform/locations_information/code_name__city_department_region.csv  ./locations_information/

# Ecraser le chemin du fichier csv
ENV LOCATION_CSV_PATH=/app/locations_information/code_name__city_department_region.csv

# Copier le "requirements.txt" dans le workdir
COPY fastapi/requirements.txt  .

# Installer les dépendances
RUN pip install  --no-cache-dir  -r requirements.txt

# Exposer le port sur lequel l'application va tourner (par défaut, FastAPI utilise 8000)
EXPOSE 8000

# Lancer fastapi avec Uvicorn <=> "uvicorn main:app --host 0.0.0.0 --port 8000" ("--reload" à éviter en prod)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
