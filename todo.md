# Reste à faire (ou pas)

## important

  1. mettre à jour la db avec psycopg

## pas urgent

  1. "1--create_csv_with_commune_departement_region_names.ipynb"

    => code Python pour télécharger les fichiers depuis le site de l'insee (extraction du .zip, etc...)


  1. évolution des données dans les tables experience et qualification => pris en compte mais le faire pour les autres tables de fait.

  1. Job_Market/load_sql/2--script_insert_into_tables.py => intégrer les transformations (Job_Market/sql_requests/0--execute_transformations.sh)

  1. Supprimer ce fichier sur le remote :
    https://github.com/vimchun/Job-Market-in-France/blob/update-db/api_extract__transform/outputs/offres/1--generated_json_file/troubleshooting/concatenation_dateExtraction_datePremiereEcriture/~%24notes.xlsx

## nice to have

  1. transformation pour avoir les années d'exp. (table experience)

  1. transformation pour avoir un attribut avec un dictionnaire avec les outils (python, sql, pyspark...) et le nombre de fois où le keyword apparaît dans la description de l'offre