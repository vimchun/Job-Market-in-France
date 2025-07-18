-- extension ".pgsql" pour tester avec l'extension vscode "PostgreSQL"...
SELECT
    metier_data
    , COUNT(*)
FROM
    descriptionoffre
WHERE
    metier_data IN ('DE' , 'DA' , 'DS')
GROUP BY
    metier_data
ORDER BY
    count DESC
