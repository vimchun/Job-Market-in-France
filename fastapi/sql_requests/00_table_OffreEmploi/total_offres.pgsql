-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
WITH latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
SELECT
    COUNT(*) AS total_offres
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
    JOIN localisation l ON l.offre_id = oe.offre_id
    -- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
    JOIN latest_date ld ON ld.latest_date_extraction = oe.date_extraction
    -- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
WHERE
    metier_data = 'placeholder_metier_data'
    AND code_region IN (placeholder_code_region)
    AND code_departement IN (placeholder_code_departement)
    AND code_postal IN (placeholder_code_postal)
    AND code_insee IN (placeholder_code_insee);