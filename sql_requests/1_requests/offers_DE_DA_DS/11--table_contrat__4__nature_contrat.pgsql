SELECT
    COUNT(*) AS total_offres
    , nature_contrat
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    nature_contrat
ORDER BY
    total_offres DESC
