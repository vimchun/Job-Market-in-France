-- -- requête pour afficher dans la colonne "liste_mots_cles" une liste
-- --  de mots-clés qui apparaissent dans la description de l'offre
--
-- add kubernetes
WITH liste_mots_cles AS (
    SELECT
        UNNEST(ARRAY[
            -- langues
            'python'
            , 'java'
            , 'scala'
            , 'bash'
            -- bdd
            , 'sql'
            , 'postgresql'
            , 'timescaledb'
            , 'ingluxdb'
            , 'elastic'
            , 'redis'
            , 'mysql'
            , 'nosql'
            , 'mongodb'
            , 'cassandra'
            -- lib/framework python
            , 'numpy'
            , 'pandas'
            , 'polars'
            , 'fastapi'
            , 'django'
            , 'flask'
            , 'scikit'
            , 'tensorflow'
            , 'pytorch'
            -- big data & data warehousing
            , 'snowflake'
            , 'databricks'
            , 'bigquery'
            -- orchestration
            , 'airflow'
            , 'luigi'
            -- environnement
            , 'notebook'
            , 'docker'
            , 'windows'
            , 'linux'
            -- git
            , 'git'
            , 'gitlab'
            , 'github'
            -- outils big data
            , 'spark'
            , 'kafka'
            , 'hadoop'
            -- outils etl
            , 'etl'
            , 'talend'
            , 'stambia'
            , 'informatica'
            , 'apache nifi'
            -- outils
            , 'dbt'
            , 'grafana'
            -- power platform
            , 'power platform'
            , 'power automate'
            , 'power apps'
            -- cloud
            , 'aws'
            , 'gcp'
            , 'azure'
            -- dataviz
            , 'power bi'
            -- , 'tableau'  -- pose problème car certaines descriptions stipulent "tableau de bord"
            , 'excel'
            -- plus pour un ds
            , 'machine learning'
            , 'nlp'
            , 'llm'
            , 'tensorflow'
            , 'deep learning'
            , 'hugging face'
            , 'keras'
            --
]) AS mot)
    -- unnest() transforme un tableau en une table
    -- Ici, on crée une "table" de mots-clés où chaque mot (Python, SQL...) sera une ligne
    , occurrences AS (
        SELECT
            dof.offre_id
            , intitule_offre
            , dof.metier_data
            , dof.description_offre
            , m.mot
            , (
                SELECT
                    COUNT(*)
                FROM
                REGEXP_MATCHES(LOWER(dof.description_offre) , m.mot , 'g')) AS nb_occurrences
            FROM
                DescriptionOffre dof
            CROSS JOIN liste_mots_cles m
        WHERE
            dof.metier_data IN ('DA' , 'DE' , 'DS'))
        SELECT
            offre_id
            , intitule_offre
            , metier_data
            , description_offre
            , ARRAY_AGG(mot) AS liste_mots_cles -- solution 1 : liste
            -- , JSON_OBJECT_AGG(mot , nb_occurrences) AS liste_mots_cles  -- solution 2 : dictionnaire
            -- Choix 1 : avec toutes les clés du json
            -- FROM
            --     occurrences
            -- Choix 2 : avec que les clés du json où les valeurs sont positives
        FROM (
            SELECT
                offre_id
                , intitule_offre
                , metier_data
                , description_offre
                , mot
                , nb_occurrences
            FROM
                occurrences
            WHERE
                nb_occurrences > 0) AS filtered_occurrences
        GROUP BY
            offre_id
            , intitule_offre
            , metier_data
            , description_offre
