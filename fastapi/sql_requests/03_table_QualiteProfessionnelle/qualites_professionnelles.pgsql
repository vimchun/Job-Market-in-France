-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
WITH latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
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
    -- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
    JOIN latest_date ld ON ld.latest_date_extraction = oe.date_extraction
    -- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
WHERE
    metier_data = 'placeholder_metier_data'
    AND code_region IN (placeholder_code_region)
    AND code_departement IN (placeholder_code_departement)
    AND code_postal IN (placeholder_code_postal)
    AND code_insee IN (placeholder_code_insee)
GROUP BY
    qp.qualite_professionnelle_libelle
    -- , qp.qualite_professionnelle_description
ORDER BY
    nombre_occurences DESC;