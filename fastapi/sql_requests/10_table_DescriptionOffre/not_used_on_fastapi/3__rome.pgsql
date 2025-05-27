SELECT
    COUNT(*) AS total_offres
    , rome_code
    , rome_libelle
    -- , appellation_rome
    -- , intitule_offre
FROM
    descriptionoffre dof
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
    -- rome_code = 'M1811'
GROUP BY
    rome_code
    , rome_libelle
    -- , appellation_rome
    -- , intitule_offre
ORDER BY
    total_offres DESC;
    -- rome_code ASC
