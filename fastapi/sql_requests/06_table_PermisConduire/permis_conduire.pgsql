-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
WITH latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
SELECT
    COUNT(pc.permis_libelle) AS nombre_occurences
    , pc.permis_libelle
    , pc.permis_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_permisconduire op ON op.offre_id = dof.offre_id
    JOIN permisconduire pc ON op.permis_id = pc.permis_id
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
    pc.permis_libelle
    , pc.permis_code_exigence
ORDER BY
    permis_code_exigence ASC --tri par E(xigé), S(ouhaité)
    , nombre_occurences DESC
    , permis_libelle ASC;

