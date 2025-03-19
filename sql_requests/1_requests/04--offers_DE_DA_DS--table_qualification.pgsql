-- Qualification les plus demandées
SELECT
    COUNT(q.qualification_code) AS nombre_occurences
    , q.qualification_libelle
FROM
    descriptionoffre dof
    JOIN offre_qualification oqp ON dof.offre_id = oqp.offre_id
    JOIN qualification q ON oqp.qualification_code = q.qualification_code
WHERE
    -- choisir le métier data ici :
    metier_data = 'DA' -- 'DE', 'DA' or 'DS'
GROUP BY
    q.qualification_libelle
ORDER BY
    nombre_occurences DESC;

