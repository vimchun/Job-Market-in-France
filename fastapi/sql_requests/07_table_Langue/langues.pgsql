-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI
WITH latest_date AS (
    SELECT
        MAX(date_extraction) AS latest_date_extraction
    FROM
        offreemploi)
-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI
SELECT
    COUNT(l.langue_libelle) AS nombre_occurences
    , l.langue_libelle
    , l.langue_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_langue ol ON ol.offre_id = dof.offre_id
    JOIN langue l ON ol.langue_id = l.langue_id
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
    JOIN localisation loc ON dof.offre_id = loc.offre_id
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
    l.langue_libelle
    , l.langue_code_exigence
ORDER BY
    langue_code_exigence ASC --tri par E(xigé), S(ouhaité)
    , nombre_occurences DESC
    , langue_libelle ASC;

