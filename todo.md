# Reste à faire (ou pas)

### à voir après soutenance (28/07/2025)

  - alert manager

  - github actions (dossier .workflow)

  - pytest

  - mettre en place dbt


### P0

  - fastapi idées :
    - création offre (id offre obligatoire, mais doit être unique)
    - suppression offre
    - ajouter une route comme /healthcheck ou /status qui permet de vérifier que la base est connectée (test SELECT 1).


### P1

  - pb avec `airflow\dags\sql\transformation_4_update__table_contrat__columns__salaire_min__salaire_max.sql` => n'écrit rien dans les colonnes ?

  - grafana : ajouter les locks/conflicts de postgres

  - airflow : activer les dags au démarrage après un reboot (possible ?)


### P2

  - script pour générer le rapport en pdf à partir des .md (avec modifs des urls)

  - pb pbi avec certaines villes mal situées (ex: Buc pas en IDF)

  - DAG 2 => option pour ne prendre en compte que les dernières offres (pour que le script tourne plus vite)

  - attribut `liste_mots_cles` : faisabilité regex sur le mot entier (exemple si on cherche le langage `R`)

  - renommer les fichiers sql en anglais ?

  - airflow : utiliser log au lieu de print ?
        log.info("") au lieu de print ?


### P3

  - pour la partie 1 :
    - Fichier en format tableau avec le nom de la source, la technique utilisée, un échantillon des données

  - transformation pour avoir les années d'exp. (table experience)

  - export db ?

  - Power BI : Sauvegarder petit fichier, puis charger pour gain de place et ouvrir le fichier plus facilement ?
