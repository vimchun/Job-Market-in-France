[Retour à la page principale](../README.md)

# 4. Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL

## 4.a. Création d'une API pour la db

- FastAPI

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.



## 4.b. Dockerisation de l'application et de la db PostGreSQL


- Arborescence avec les éléments importants

  - Le fichier `Job_Market/fastapi/requirements.txt` ne contient que les dépendances utiles pour pouvoir lancer le script `Job_Market/fastapi/main.py`.

- en mode "dev" :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]` (avec l'option `--reload` pour ne pas avoir à relancer la commande après une modification)
  - `docker-compose.yml` :
    - avec les montages de volumes pour ne pas avoir à relancer `docker-compose up` après chaque modification

- passage en mode "prod" quand les devs sont terminés :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` (sans l'option `--reload`)
    - `COPY` du script python, et des fichiers nécessaires dans le conteneur (fichier csv, fichiers sql)

