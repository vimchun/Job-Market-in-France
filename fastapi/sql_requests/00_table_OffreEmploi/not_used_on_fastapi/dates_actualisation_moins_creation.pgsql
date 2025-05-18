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
    metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    date_extraction
    , date_creation
    , date_actualisation
ORDER BY
    -- total_offres DESC
    date_diff DESC
