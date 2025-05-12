SELECT
    COUNT(*) AS total_offres
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
WHERE
    metier_data = 'placeholder_metier_data' -- placeholder remplacé dans le script python (ou 'DE'|'DA'|'DS' si le script est exécuté en dehors de python)
    AND date_creation >= 'placeholder_date_creation_min' -- placeholder remplacé dans le script python (ou '2025-04-10' si le script est exécuté en dehors de python)