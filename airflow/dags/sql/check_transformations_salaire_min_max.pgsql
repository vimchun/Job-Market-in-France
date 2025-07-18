-- extension ".pgsql" pour tester avec l'extension vscode "PostgreSQL"...
-- SELECT
--     COUNT(*) FILTER (WHERE salaire_min IS NOT NULL) AS "nb offres avec salaire min"
--     , COUNT(*) FILTER (WHERE salaire_max IS NOT NULL) AS "nb offres avec salaire max"
-- FROM
--     contrat;

----------------------

-- SELECT
--     -- offre_id
--     -- , salaire_min
--     -- , salaire_max
--     -- , salaire_libelle
--     *
-- FROM
--     contrat
-- WHERE
--     salaire_libelle IS NOT NULL
--     --     salaire_min IS NOT NULL
--     --     OR salaire_max IS NOT NULL
-- LIMIT 100;

----------------------

-- Partie 1 du script :

SELECT
    salaire_libelle
    , CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') -- REGEXP_REPLACE() recherche "." ou "," suivi d'exactement 1 ou 2 chiffres, et supprime ce pattern (supprime les centimes de "salaire_libelle")
            , '(\d+)') -- REGEXP_SUBSTR() extrait le premier groupe de chiffres
        AS INTEGER) AS get_salaire_min
    , CAST(REGEXP_SUBSTR (REGEXP_REPLACE(salaire_libelle , '[.,]\d{1,2}' , '') -- REGEXP_REPLACE() recherche "." ou "," suivi d'exactement 1 ou 2 chiffres, et supprime ce pattern (supprime les centimes de "salaire_libelle")
            , '(\d+)' , 1 , 2) -- REGEXP_SUBSTR() extrait le second groupe de chiffres
        AS INTEGER) AS get_salaire_max
FROM
    contrat
WHERE
    salaire_libelle IS NOT NULL
LIMIT 10;

