WITH offres_filtrees AS (
    SELECT
        *
    FROM
        descriptionoffre
    WHERE
        metier_data = 'placeholder_metier_data'
)
, total_offres AS (
    SELECT
        COUNT(*) AS total
    FROM
        offres_filtrees
)
-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
, latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI

SELECT
    COUNT(*) AS total_offres_departement
    , CONCAT(ROUND(COUNT(*) * 100.0 / tof.total , 1) , ' pourcent') AS pourcentage -- mettre le signe du pourcentage pose un problème côté psycopg (par rapport aux "pourcentage s" (placeholder))
    , nom_departement
FROM
    localisation l
    JOIN offres_filtrees ofi ON ofi.offre_id = l.offre_id
    JOIN total_offres tof ON 1 = 1 -- pour avoir le nombre d'offres total (constante) pour chaque ligne de la table de gauche
    JOIN offreemploi oe ON l.offre_id = oe.offre_id
    -- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
    JOIN latest_date ld ON ld.latest_date_extraction = oe.date_extraction
    -- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
WHERE
    nom_departement IS NOT NULL
GROUP BY
    nom_departement
    , tof.total
ORDER BY
    total_offres_departement DESC
LIMIT 30;