SELECT
    COUNT(*) AS total_offres
    , accessible_travailleurs_handicapes
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    accessible_travailleurs_handicapes
ORDER BY
    total_offres DESC;

