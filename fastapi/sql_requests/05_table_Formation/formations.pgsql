SELECT
    COUNT(f.formation_code) AS nombre_occurences
    , f.formation_code
    , f.formation_domaine_libelle
    , f.formation_niveau_libelle
    , f.formation_commentaire
    , f.formation_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_formation ofo ON dof.offre_id = ofo.offre_id
    JOIN formation f ON ofo.formation_id = f.formation_id
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
    f.formation_code
    , f.formation_domaine_libelle
    , f.formation_niveau_libelle
    , f.formation_commentaire
    , f.formation_code_exigence
HAVING
    COUNT(f.formation_code) > 0
ORDER BY
    formation_code_exigence ASC --tri par E(xigé), S(ouhaité)
    , nombre_occurences DESC
    , f.formation_code ASC
    , f.formation_niveau_libelle ASC;

