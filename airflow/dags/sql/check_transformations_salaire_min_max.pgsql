-- extension ".pgsql" pour tester avec l'extension vscode "PostgreSQL"...
SELECT
    COUNT(*) FILTER (WHERE salaire_min IS NOT NULL) AS "nb offres avec salaire min"
    , COUNT(*) FILTER (WHERE salaire_max IS NOT NULL) AS "nb offres avec salaire max"
FROM
    contrat;

