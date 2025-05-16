SELECT
    COUNT(qp.qualite_professionnelle_libelle) AS nombre_occurences
    , qp.qualite_professionnelle_libelle
    , qp.qualite_professionnelle_description
FROM
    descriptionoffre dof
    JOIN offre_qualiteprofessionnelle oqp ON dof.offre_id = oqp.offre_id
    JOIN qualiteprofessionnelle qp ON oqp.qualite_professionnelle_id = qp.qualite_professionnelle_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    qp.qualite_professionnelle_libelle
    , qp.qualite_professionnelle_description
ORDER BY
    nombre_occurences DESC;