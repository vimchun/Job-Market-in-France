WITH total_offres AS (
    SELECT
        COUNT(*) AS total
    FROM
        descriptionoffre
    WHERE
        metier_data = 'placeholder_metier_data'
)
    -- La CTE renvoie le nombre d'offres total (constante)
    SELECT
        COUNT(*) AS total_offres_region
        , CONCAT(ROUND(COUNT(*) * 100.0 / tof.total , 1) , ' pourcent') AS pourcentage -- mettre le signe du pourcentage pose un problème côté psycopg (par rapport aux "pourcentage s" (placeholder))
        , nom_region
    FROM
        localisation l
        JOIN descriptionoffre dof ON dof.offre_id = l.offre_id
        JOIN total_offres tof ON 1 = 1 -- pour avoir le nombre d'offres total (constante) pour chaque ligne de la table de gauche
    WHERE
        metier_data = 'placeholder_metier_data'
        AND nom_region IS NOT NULL
    GROUP BY
        nom_region
        , tof.total
    ORDER BY
        total_offres_region DESC;

