WITH total_offres AS (
    SELECT
        COUNT(*) AS total
    FROM
        descriptionoffre
    -- WHERE
        -- metier_data = 'placeholder_metier_data' -- placeholder which will be replaced on the FastAPI python script
        -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
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
        metier_data = 'placeholder_metier_data' -- placeholder which will be replaced on the FastAPI python script
        -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
        -- AND nom_ville IS NOT NULL
    GROUP BY
        nom_ville
        , tof.total
    ORDER BY
        total_offres_ville DESC
    LIMIT 20;

