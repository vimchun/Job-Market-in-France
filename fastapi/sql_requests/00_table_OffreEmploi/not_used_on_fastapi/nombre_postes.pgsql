SELECT
    COUNT(*) AS total_offres
    , nombre_postes
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON oe.offre_id = dof.offre_id
WHERE
    -- metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    nombre_postes
ORDER BY
    total_offres DESC
