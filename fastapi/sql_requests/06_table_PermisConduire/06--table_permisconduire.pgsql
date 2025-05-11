SELECT
    COUNT(pc.permis_libelle) AS nombre_occurences
    , pc.permis_libelle
    , pc.permis_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_permisconduire op ON op.offre_id = dof.offre_id
    JOIN permisconduire pc ON op.permis_id = pc.permis_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    pc.permis_libelle
    , pc.permis_code_exigence
ORDER BY
    nombre_occurences DESC;

