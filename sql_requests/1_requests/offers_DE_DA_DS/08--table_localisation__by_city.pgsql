WITH total_offres AS (
    SELECT
        COUNT(*) AS total
    FROM
        descriptionoffre
    WHERE
        metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
)
    -- La CTE renvoie le nombre d'offres total pour 'DE', 'DA' ou 'DS' (constante)
    SELECT
        COUNT(*) AS total_offres_ville
        , CONCAT(ROUND(COUNT(*) * 100.0 / tof.total , 1) , ' %') AS pourcentage
        , nom_ville
    FROM
        localisation l
        JOIN descriptionoffre dof ON dof.offre_id = l.offre_id
        JOIN total_offres tof ON 1 = 1 -- pour avoir le nombre d'offres total (constante) pour chaque ligne de la table de gauche
    WHERE
        metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
        -- AND nom_ville IS NOT NULL
    GROUP BY
        nom_ville
        , tof.total
    ORDER BY
        total_offres_ville DESC
    LIMIT 15;

