[Retour à la page principale](../README.md)

# 4. Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL

## 4.a. Création d'une API pour la db

- FastAPI

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.



## 4.b. Dockerisation de l'application et de la db PostGreSQL

- Le fichier `Job_Market/fastapi/requirements.txt` ne contient que les dépendances utiles pour pouvoir lancer le script `Job_Market/fastapi/main.py`.

- `docker-compose.yml` en mode dev avec les montages de volumes.

- Arborescence avec les éléments importants
