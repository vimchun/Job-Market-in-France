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
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    c.competence_code
    , c.competence_code_exigence
    , c.competence_libelle
ORDER BY
    competence_code_exigence ASC -- E(xigé) puis S(ouhaité)
    , nombre_occurences DESC;

