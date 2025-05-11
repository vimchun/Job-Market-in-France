SELECT
    COUNT(*) AS total_offres
    -- , nom_entreprise
    , code_naf
    , secteur_activite_libelle
FROM
    descriptionoffre dof
    JOIN entreprise e ON dof.offre_id = e.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    -- nom_entreprise
    code_naf
    , secteur_activite_libelle
HAVING
    code_naf IS NOT NULL
ORDER BY
    total_offres DESC
    -- , nom_entreprise ASC
    , code_naf ASC;

