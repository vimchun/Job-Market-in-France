-- Pour réinitialiser la colonne :
-- UPDATE DescriptionOffre
-- SET liste_mots_cles = NULL;
--
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
            , 'power automate' -- pas de e volontairement
            , 'power apps'
            -- cloud
            , 'aws'
            , 'gcp'
            , 'azure'
            -- dataviz
            , 'power bi'
            , 'tableau'
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
            , dof.intitule_offre
            , dof.metier_data
            , dof.description_offre
            , m.mot
        FROM
            DescriptionOffre dof
        CROSS JOIN liste_mots_cles m
    WHERE
        LOWER(dof.description_offre)
        LIKE '%' || LOWER(m.mot) || '%' -- insensible à la casse
        AND dof.metier_data IN ('DA' , 'DE' , 'DS'))
UPDATE
    DescriptionOffre dof
SET
    liste_mots_cles = subquery.liste_mots_cles
FROM (
    SELECT
        offre_id
        , ARRAY_AGG(DISTINCT mot) AS liste_mots_cles -- liste distincte des mots trouvés dans la description
    FROM
        occurrences
    GROUP BY
        offre_id) AS subquery
WHERE
    dof.offre_id = subquery.offre_id;

