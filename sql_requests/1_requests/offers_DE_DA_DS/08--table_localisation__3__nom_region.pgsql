WITH total_offres AS (
    SELECT
        COUNT(*) AS total
    FROM
        descriptionoffre
    WHERE
        -- choisir le métier data ici :
        metier_data = 'DE' -- 'DE', 'DA' ou 'DS'
)
    -- La CTE renvoie le nombre d'offres total pour 'DE', 'DA' ou 'DS' (constante)
    SELECT
        COUNT(*) AS total_offres_region
        , CONCAT(ROUND(COUNT(*) * 100.0 / tof.total , 1) , ' %') AS pourcentage
        , nom_region
    FROM
        localisation l
        JOIN descriptionoffre dof ON dof.offre_id = l.offre_id
        JOIN total_offres tof ON 1 = 1 -- pour avoir le nombre d'offres total (constante) pour chaque ligne de la table de gauche
    WHERE
        metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
        AND nom_region IS NOT NULL
    GROUP BY
        nom_region
        , tof.total
    ORDER BY
        total_offres_region DESC;

