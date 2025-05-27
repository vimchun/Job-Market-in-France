[Retour à la page principale](../README.md)

# 4. Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL

## 4.a. Création d'une API pour la db

- Utilisation de `FastAPI`.

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.



## 4.b. Dockerisation de l'application et de la db PostGreSQL

- Arborescence avec les éléments importants liés à la dockerisation :

  .
  ├── api_extract__transform
  │   ├── locations_information
  │   │   ├── code_name__city_department_region.csv   # fichier utilisé par le script fastapi
  │  
  ├── fastapi/                                        # application FastAPI
  │   ├── Dockerfile                                  # construction du conteneur FastAPI
  │   ├── locations_information                       # point de montage (volume)  # todo : à renommer en "locations_information_mount" ?
  │   ├── main.py                                     # script fastapi
  │   ├── requirements.txt                            # dépendances pour pouvoir lancer le script fastapi dans le conteneur
  │   └── sql_requests                                # requêtes SQL utilisées par le script fastapi
  │  
  ├── docker-compose.yml                              # orchestration docker pour postgres + fastapi



- Travail en mode "dev" :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]` (avec l'option `--reload` pour ne pas avoir à relancer la commande après une modification)
  - `docker-compose.yml` :
    - avec les montages de volumes pour ne pas avoir à relancer le docker-compose après chaque modification de fichiers sql

- passage en mode "prod" quand les devs sont terminés :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` (sans l'option `--reload`)
    - `COPY` du script python, et des fichiers nécessaires dans le conteneur (fichier csv, fichiers sql), au lieu de passer par des volumes