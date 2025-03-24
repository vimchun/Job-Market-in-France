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
WHERE
    metier_data = 'DE' -- choisir entre 'DE', 'DA' or 'DS'
GROUP BY
    f.formation_code
    , f.formation_domaine_libelle
    , f.formation_niveau_libelle
    , f.formation_commentaire
    , f.formation_code_exigence
ORDER BY
    nombre_occurences DESC;

