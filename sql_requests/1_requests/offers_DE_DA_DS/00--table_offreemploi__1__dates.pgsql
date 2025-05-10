SELECT
    COUNT(*) AS total_offres
    , date_extraction
    , date_creation
    , date_actualisation
    , date_actualisation - date_creation AS date_diff
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON oe.offre_id = dof.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder qui sera remplacé dans "Job_Market/fastapi/fastapi.py"
    -- metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    date_extraction
    , date_creation
    , date_actualisation
ORDER BY
    -- total_offres DESC
    date_diff DESC
