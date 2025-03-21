SELECT
    COUNT(*) AS total_offres
    , nom_partenaire
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    nom_partenaire
ORDER BY
    total_offres DESC;

