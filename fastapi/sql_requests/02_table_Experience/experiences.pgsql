SELECT
    COUNT(e.experience_libelle) AS nombre_occurences
    , e.experience_libelle
    , e.experience_commentaire
    , e.experience_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_experience oex ON dof.offre_id = oex.offre_id
    JOIN experience e ON oex.experience_id = e.experience_id
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
    e.experience_libelle
    , e.experience_commentaire
    , e.experience_code_exigence
ORDER BY
    -- tri par D(ébutant), S(ouhaité), E(xigé)
    CASE experience_code_exigence
    WHEN 'D' THEN
        1
    WHEN 'S' THEN
        2
    WHEN 'E' THEN
        3
    END
    -- puis tri par experience_libelle
    , nombre_occurences DESC
    , experience_libelle ASC;