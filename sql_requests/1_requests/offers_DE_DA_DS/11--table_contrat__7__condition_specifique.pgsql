SELECT
    COUNT(*) AS total_offres
    , condition_specifique
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    condition_specifique  -- enlever le filtre "metier_data" pour voir toutes les valeurs possibles
ORDER BY
    total_offres DESC
