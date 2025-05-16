SELECT
    COUNT(*) AS total_offres
    , nom_entreprise
    , entreprise_adaptee
FROM
    descriptionoffre dof
    JOIN entreprise e ON dof.offre_id = e.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    nom_entreprise
    , entreprise_adaptee
ORDER BY
    total_offres DESC,
    entreprise_adaptee DESC,
    nom_entreprise ASC
