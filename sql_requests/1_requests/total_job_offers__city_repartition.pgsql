SELECT
    nom_ville
    , COUNT(*) AS total_offres
    , CONCAT(ROUND((COUNT(*) * 100.0) / (
            SELECT
                COUNT(*)
            FROM localisation) , 1) , ' %') AS pourcentage
FROM
    localisation
GROUP BY
    nom_ville
HAVING
    nom_ville IS NOT NULL
ORDER BY
    total_offres DESC
LIMIT 20;

