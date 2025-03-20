SELECT
    COUNT(e.experience_libelle) AS nombre_occurences
    , e.experience_libelle
    , e.experience_code_exigence
    , e.experience_commentaire
FROM
    descriptionoffre dof
    JOIN offre_experience oe ON dof.offre_id = oe.offre_id
    JOIN experience e ON oe.experience_id = e.experience_id
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    e.experience_libelle
    , e.experience_code_exigence
    , e.experience_commentaire
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
    , experience_libelle ASC;