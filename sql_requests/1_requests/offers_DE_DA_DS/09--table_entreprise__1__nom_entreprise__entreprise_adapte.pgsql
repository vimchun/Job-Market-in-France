SELECT
    COUNT(*) AS total_offres
    , nom_entreprise
    , entreprise_adaptee
FROM
    descriptionoffre dof
    JOIN entreprise e ON dof.offre_id = e.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    nom_entreprise
    , entreprise_adaptee
ORDER BY
    total_offres DESC,
    entreprise_adaptee DESC,
    nom_entreprise ASC
