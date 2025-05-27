SELECT
    COUNT(*) AS total_offres
    , nom_partenaire
FROM
    descriptionoffre dof
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    nom_partenaire
ORDER BY
    total_offres DESC;

