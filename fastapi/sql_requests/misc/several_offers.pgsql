-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
WITH latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
SELECT
    ofe.offre_id AS offre
    , intitule_offre
    , date_creation
    , date_actualisation
    , nom_ville
    , nom_departement
    , nom_region
    -- , url_france_travail
FROM
    offreemploi ofe
    JOIN descriptionoffre dof ON ofe.offre_id = dof.offre_id
    JOIN contrat c ON c.offre_id = dof.offre_id
    JOIN localisation loc ON loc.offre_id = dof.offre_id
    -- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
    JOIN latest_date ld ON ld.latest_date_extraction = ofe.date_extraction
    -- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
WHERE
    metier_data = 'placeholder_metier_data'
    AND code_region IN (placeholder_code_region)
    AND code_departement IN (placeholder_code_departement)
    AND code_postal IN (placeholder_code_postal)
    AND code_insee IN (placeholder_code_insee)
ORDER BY
    date_creation DESC
LIMIT 10;