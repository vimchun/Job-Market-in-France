-- extension ".pgsql" pour tester avec l'extension vscode "PostgreSQL"...
SELECT
    COUNT(*) as "total offres avec mots-clés"
FROM
    descriptionoffre
WHERE
    liste_mots_cles IS NOT NULL;