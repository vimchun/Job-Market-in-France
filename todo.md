# Reste à faire (ou pas)

### P0

  - airflow :
    - lancer script 1 puis script 2 (fréquence à définir)

  - github actions (dossier .workflow)

  - ajout prom/grafana au docker compose

### P1

  - mettre en place dbt ?

  - airflow : utiliser log au lieu de print ?
        log.info("") au lieu de print ?

### P2

  - fastapi idées :
    - création offre (id offre obligatoire, mais doit être unique)
    - suppression offre
    - ajouter une route comme /healthcheck ou /status qui permet de vérifier que la base est connectée (test SELECT 1).

  - script "2--script_insert_into_tables.py" => option pour ne prendre en compte que les dernières offres (pour que le script tourne plus vite)

  - attribut `liste_mots_cles` : faisabilité regex sur le mot entier (exemple si on cherche le langage `R`)

  - renommer les fichiers sql en anglais ?


### P3

  - pour la partie 1 :
    - Fichier en format tableau avec le nom de la source, la technique utilisée, un échantillon des données

  - transformation pour avoir les années d'exp. (table experience)

  - export db ?