# Reste à faire (ou pas)

### à voir après soutenance (28/07/2025)

  - alert manager

  - github actions (dossier .workflow)

  - pytest

  - mettre en place dbt


### P0

  - fastapi idées :

    - tag : pour une offre:

      - création offre
        - id offre obligatoire, mais doit être unique

      - suppression offre

      - afficher 10 premières offres DE / DA... dispo ou pas... => ajout url



  - remplir tables : ajout url pour postuler

        "origineOffre": {
            "origine": "2",
            "urlOrigine": "https://candidat.francetravail.fr/offres/recherche/detail/9635836",
        }



### P1

  - pb avec `airflow\dags\sql\transformation_4_update__table_contrat__columns__salaire_min__salaire_max.sql`
  => n'écrit rien dans les colonnes ?
  => résolu par la suppression des leading/trailing " ???


  - grafana : ajouter les locks/conflicts de postgres

  - airflow : activer les dags au démarrage après un reboot (possible ?)

  - mettre description_offre de la table descriptionoffre dans un fichier à part (trop gros)

### P2

  - script pour générer le rapport en pdf à partir des .md (avec modifs des urls)

  - pb pbi avec certaines villes mal situées (ex: Buc pas en IDF)

  - DAG 2 => option pour ne prendre en compte que les dernières offres (pour que le script tourne plus vite)

  - attribut `liste_mots_cles` : faisabilité regex sur le mot entier (exemple si on cherche le langage `R`)

  - renommer les fichiers sql en anglais ?

  - airflow : utiliser log au lieu de print ?
        log.info("") au lieu de print ?

  - fastapi idées :

    - ajouter une route comme /healthcheck ou /status qui permet de vérifier que la base est connectée (test SELECT 1).
    - ajouter une route qui fait le "docker ps"


### P3

  - pour la partie 1 :
    - Fichier en format tableau avec le nom de la source, la technique utilisée, un échantillon des données

  - transformation pour avoir les années d'exp. (table experience)

  - export db ?

  - Power BI : Sauvegarder petit fichier, puis charger pour gain de place et ouvrir le fichier plus facilement ?
