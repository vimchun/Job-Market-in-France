SELECT
    COUNT(*) AS total_offres
    , duree_travail_libelle
    , duree_travail_libelle_converti
    , temps_travail
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    duree_travail_libelle
    , duree_travail_libelle_converti
    , temps_travail
ORDER BY
    total_offres DESC
