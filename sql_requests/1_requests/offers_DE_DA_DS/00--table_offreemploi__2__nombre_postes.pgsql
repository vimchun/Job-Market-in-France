SELECT
    COUNT(*) AS total_offres
    , nombre_postes
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON oe.offre_id = dof.offre_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    nombre_postes
ORDER BY
    total_offres DESC
