SELECT
    nom_region
    , COUNT(*) AS total_offres
    , CONCAT(ROUND((COUNT(*) * 100.0) / (
            SELECT
                COUNT(*)
            FROM localisation) , 1) , ' %') AS pourcentage
FROM
    localisation
GROUP BY
    nom_region
HAVING
    nom_region IS NOT NULL
ORDER BY
    total_offres DESC;

