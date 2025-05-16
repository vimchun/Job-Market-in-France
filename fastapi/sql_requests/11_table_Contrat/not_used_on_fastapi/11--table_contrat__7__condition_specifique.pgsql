SELECT
    COUNT(*) AS total_offres
    , condition_specifique
FROM
    descriptionoffre dof
    JOIN contrat c ON c.offre_id = dof.offre_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    condition_specifique  -- enlever le filtre "metier_data" pour voir toutes les valeurs possibles
ORDER BY
    total_offres DESC
