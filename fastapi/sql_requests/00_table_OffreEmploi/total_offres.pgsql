SELECT
    COUNT(*) AS total_offres
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
    JOIN localisation l ON l.offre_id = oe.offre_id
WHERE
    metier_data = 'placeholder_metier_data'
    AND date_creation >= 'placeholder_date_creation_min'
    AND code_region IN (placeholder_code_region)
    AND nom_region IN (placeholder_nom_region)
    AND code_departement IN (placeholder_code_departement)
    AND nom_departement IN (placeholder_nom_departement)
    AND code_postal IN (placeholder_code_postal)
    AND nom_ville IN (placeholder_nom_ville);