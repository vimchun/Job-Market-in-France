SELECT
    COUNT(qp.qualite_professionnelle_libelle) AS nombre_occurences
    , qp.qualite_professionnelle_libelle
    -- , qp.qualite_professionnelle_description
FROM
    descriptionoffre dof
    JOIN offre_qualiteprofessionnelle oqp ON dof.offre_id = oqp.offre_id
    JOIN qualiteprofessionnelle qp ON oqp.qualite_professionnelle_id = qp.qualite_professionnelle_id
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
    JOIN localisation l ON dof.offre_id = l.offre_id
WHERE
    metier_data = 'placeholder_metier_data'
    AND date_creation >= 'placeholder_date_creation_min'
    AND code_region IN (placeholder_code_region)
    AND nom_region IN (placeholder_nom_region)
    AND code_departement IN (placeholder_code_departement)
    AND nom_departement IN (placeholder_nom_departement)
    AND code_postal IN (placeholder_code_postal)
    AND nom_ville IN (placeholder_nom_ville)
GROUP BY
    qp.qualite_professionnelle_libelle
    -- , qp.qualite_professionnelle_description
ORDER BY
    nombre_occurences DESC;