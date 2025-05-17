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
    pc.permis_libelle
    , pc.permis_code_exigence
ORDER BY
    --tri par E(xigé), S(ouhaité)
    permis_code_exigence ASC
    , nombre_occurences DESC
    , permis_libelle ASC;

