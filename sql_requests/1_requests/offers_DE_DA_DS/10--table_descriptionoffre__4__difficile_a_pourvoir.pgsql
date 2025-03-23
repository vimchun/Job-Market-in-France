SELECT
    COUNT(*) AS total_offres
    , difficile_a_pourvoir
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    difficile_a_pourvoir
ORDER BY
    total_offres DESC;

