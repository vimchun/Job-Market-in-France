SELECT
    ofe.offre_id as offre
    , intitule_offre
    , date_creation
    , nom_ville
    , nom_departement
    , nom_region
    , metier_data
    -- , salaire_min
    -- , salaire_max
    , dof.liste_mots_cles
    , dof.description_offre
FROM
    offreemploi ofe
    JOIN descriptionoffre dof ON ofe.offre_id = dof.offre_id
    JOIN contrat c ON c.offre_id = dof.offre_id
    JOIN localisation loc ON loc.offre_id = dof.offre_id
WHERE
    ofe.offre_id = %s;

