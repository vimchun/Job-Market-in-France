SELECT
    COUNT(c.competence_libelle) AS nombre_occurences
    , c.competence_code
    , c.competence_libelle
    , c.competence_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_competence oc ON dof.offre_id = oc.offre_id
    JOIN competence c ON oc.competence_id = c.competence_id
WHERE
    metier_data = 'placeholder_metier_data'  -- placeholder which will be replaced on the FastAPI python script
    -- metier_data = 'DE' -- possible values : 'DE', 'DA' or 'DS' (if sql script is executed outside python script)
GROUP BY
    c.competence_code
    , c.competence_code_exigence
    , c.competence_libelle
ORDER BY
    competence_code_exigence ASC -- E(xigé) puis S(ouhaité)
    , nombre_occurences DESC;

