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
    l.langue_libelle
    , l.langue_code_exigence
ORDER BY
    --tri par E(xigé), S(ouhaité)
    langue_code_exigence ASC
    , nombre_occurences DESC
    , langue_libelle ASC;

