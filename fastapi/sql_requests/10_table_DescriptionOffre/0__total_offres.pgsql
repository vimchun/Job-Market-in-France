SELECT
    COUNT(*) AS total_offres
FROM
    descriptionoffre dof
    JOIN offreemploi oe ON dof.offre_id = oe.offre_id
WHERE
    metier_data = 'placeholder_metier_data' -- placeholder replaced on python script (or 'DE' | 'DA' | 'DS' if sql script executed outside python)
    AND date_creation >= 'placeholder_date_min' -- placeholder replaced on python script (or '2025-04-10' if sql script executed outside python)