SELECT
    COUNT(q.qualification_code) AS nombre_occurences
    , q.qualification_libelle
FROM
    descriptionoffre dof
    JOIN offre_qualification oqp ON dof.offre_id = oqp.offre_id
    JOIN qualification q ON oqp.qualification_code = q.qualification_code
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
    q.qualification_libelle
ORDER BY
    nombre_occurences DESC;

