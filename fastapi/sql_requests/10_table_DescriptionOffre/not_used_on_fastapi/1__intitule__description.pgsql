SELECT
    COUNT(*) AS total_offres
    , intitule_offre
    , description_offre
FROM
    descriptionoffre dof
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    intitule_offre
    , description_offre
ORDER BY
    total_offres DESC
LIMIT 20
