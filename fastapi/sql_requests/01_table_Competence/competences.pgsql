SELECT
    COUNT(c.competence_libelle) AS nombre_occurences
    , c.competence_code
    , c.competence_libelle
    , c.competence_code_exigence
FROM
    descriptionoffre dof
    JOIN offre_competence oc ON dof.offre_id = oc.offre_id
    JOIN competence c ON oc.competence_id = c.competence_id
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
WHERE
    metier_data = 'placeholder_metier_data' -- placeholder remplacé dans le script python (ou 'DE'|'DA'|'DS' si le script est exécuté en dehors de python)
    AND date_creation >= 'placeholder_date_creation_min' -- placeholder remplacé dans le script python (ou '2025-04-10' si le script est exécuté en dehors de python)
    -- metier_data = 'DE' -- placeholder remplacé dans le script python (ou 'DE'|'DA'|'DS' si le script est exécuté en dehors de python)
    -- AND date_creation >= '2025-04-01' -- placeholder remplacé dans le script python (ou '2025-04-10' si le script est exécuté en dehors de python)
GROUP BY
    c.competence_code
    , c.competence_code_exigence
    , c.competence_libelle
ORDER BY
    competence_code_exigence ASC -- E(xigé) puis S(ouhaité)
    , nombre_occurences DESC
    , competence_code ASC;
