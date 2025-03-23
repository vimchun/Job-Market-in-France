SELECT
    COUNT(*) AS total_offres
    , salaire_libelle
    , salaire_complement_1
    , salaire_complement_2
    , salaire_commentaire
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    salaire_libelle
    , salaire_complement_1
    , salaire_complement_2
    , salaire_commentaire
ORDER BY
    total_offres DESC
