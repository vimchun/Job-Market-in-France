SELECT
    COUNT(*) AS total_offres
    , type_contrat
    , type_contrat_libelle
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    type_contrat
    , type_contrat_libelle
ORDER BY
    total_offres DESC
