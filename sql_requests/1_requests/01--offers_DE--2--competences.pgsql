-- Compétences les plus demandées
SELECT
    -- dof.offre_id
    -- , dof.intitule_offre
    COUNT(c.competence_code) AS nombre_occurences
    , c.competence_code
    , c.competence_libelle
FROM
    descriptionoffre dof
    JOIN offre_competence oc ON dof.offre_id = oc.offre_id
    JOIN competence c ON oc.competence_id = c.competence_id
WHERE
    metier_data = 'DE'
    AND competence_code IS NOT NULL
GROUP BY
    c.competence_code
    , c.competence_libelle
ORDER BY
    nombre_occurences DESC
