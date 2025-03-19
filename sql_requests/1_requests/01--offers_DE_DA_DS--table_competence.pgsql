-- Compétences les plus demandées
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
    -- choisir le métier data ici :
    metier_data = 'DA' -- 'DE', 'DA' or 'DS'
    -- AND competence_code_exigence = 'E'
GROUP BY
    c.competence_code
    , c.competence_code_exigence
    , c.competence_libelle
ORDER BY
    nombre_occurences DESC
