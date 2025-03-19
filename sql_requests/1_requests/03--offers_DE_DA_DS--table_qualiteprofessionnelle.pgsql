-- Qualités professionnelles les plus demandées
SELECT
    COUNT(qp.qualite_professionnelle_libelle) AS nombre_occurences
    , qp.qualite_professionnelle_libelle
    -- , qp.qualite_professionnelle_description
FROM
    descriptionoffre dof
    JOIN offre_qualiteprofessionnelle oqp ON dof.offre_id = oqp.offre_id
    JOIN qualiteprofessionnelle qp ON oqp.qualite_professionnelle_id = qp.qualite_professionnelle_id
WHERE
    -- choisir le métier data ici :
    metier_data = 'DS' -- 'DE', 'DA' or 'DS'
GROUP BY
    qp.qualite_professionnelle_libelle
    , qp.qualite_professionnelle_description
ORDER BY
    nombre_occurences DESC;