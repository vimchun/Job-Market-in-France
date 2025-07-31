# Reste à faire (ou pas)

### à voir après soutenance (28/07/2025)

  - `Alert Manager` (pas très utile dans mon cas d'utilisation, car mon pc portable ne tourne pas en permanence)

  - CI/CD avec `Github Actions` / `Pytest`

  - `DBT`

  - Appli plus "conviviale" que swagger (streamlit ?)

  - Configurer `Power BI` pour exploiter les APIs ?

  - Même projet mais sur le `cloud` ?


### P0

  - données sensibles du "docker compose" à part


### P1

  - fastapi : gérer les cas d'erreur

  - airflow : activer les dags au démarrage après un reboot (possible ?)

  - mettre description_offre de la table descriptionoffre dans un fichier à part (trop gros)


### P2

  - fastapi : sécurité fastapi

  - pb pbi avec certaines villes mal situées (ex: Buc pas en IDF)

  - DAG 2 => option pour ne prendre en compte que les dernières offres (pour que le script tourne plus vite)

  - attribut `liste_mots_cles` : faisabilité regex sur le mot entier (exemple si on cherche le langage `R`)

  - airflow : utiliser log au lieu de print ?
        log.info("") au lieu de print ?

  - fastapi idées :

    - ajouter une route comme /healthcheck ou /status qui permet de vérifier que la base est connectée (test SELECT 1).
    - ajouter une route qui fait le "docker ps"


### P3

  - renommer les fichiers sql en anglais ?

  - pour la partie 1 :
    - Fichier en format tableau avec le nom de la source, la technique utilisée, un échantillon des données

  - transformation pour avoir les années d'exp. (table experience)

  - export db ?

  - Power BI : Sauvegarder petit fichier, puis charger pour gain de place et ouvrir le fichier plus facilement ?
