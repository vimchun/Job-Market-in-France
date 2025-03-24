SELECT
    COUNT(*) AS total_offres
    , rome_code
    , rome_libelle
    -- , appellation_rome
    -- , intitule_offre
FROM
    descriptionoffre dof
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
    -- rome_code = 'M1811'
GROUP BY
    rome_code
    , rome_libelle
    -- , appellation_rome
    -- , intitule_offre
ORDER BY
    total_offres DESC;
    -- rome_code ASC
