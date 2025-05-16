SELECT
    COUNT(*) AS total_offres
    , deplacement_code
    , deplacement_libelle
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    deplacement_code
    , deplacement_libelle
ORDER BY
    total_offres DESC
