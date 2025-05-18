SELECT
    COUNT(c.competence_libelle) AS nombre_occurences
    , c.competence_code
    , c.competence_libelle
    , c.competence_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_competence oc ON dof.offre_id = oc.offre_id
    JOIN competence c ON oc.competence_id = c.competence_id
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
    JOIN localisation l ON dof.offre_id = l.offre_id
WHERE
    metier_data = 'placeholder_metier_data'
    AND date_creation >= 'placeholder_date_creation_min'
    AND code_region IN (placeholder_code_region)
    AND code_departement IN (placeholder_code_departement)
    AND code_postal IN (placeholder_code_postal)
    AND code_insee IN (placeholder_code_insee)
GROUP BY
    c.competence_code
    , c.competence_code_exigence
    , c.competence_libelle
ORDER BY
    competence_code_exigence ASC -- E(xigé) puis S(ouhaité)
    , nombre_occurences DESC
    , competence_code ASC;

