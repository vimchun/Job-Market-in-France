SELECT
    COUNT(*) AS total_offres
    , duree_travail_libelle
    , duree_travail_libelle_converti
    , temps_travail
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    duree_travail_libelle
    , duree_travail_libelle_converti
    , temps_travail
ORDER BY
    total_offres DESC
