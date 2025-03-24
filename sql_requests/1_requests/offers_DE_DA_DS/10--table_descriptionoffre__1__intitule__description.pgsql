SELECT
    COUNT(*) AS total_offres
    , intitule_offre
    , description_offre
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    intitule_offre
    , description_offre
ORDER BY
    total_offres DESC
LIMIT 20
