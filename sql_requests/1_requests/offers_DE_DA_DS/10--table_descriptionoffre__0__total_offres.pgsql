SELECT
    COUNT(*) AS total_offres
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
ORDER BY
    total_offres DESC
