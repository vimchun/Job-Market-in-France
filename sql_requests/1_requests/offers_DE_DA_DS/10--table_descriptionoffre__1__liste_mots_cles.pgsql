SELECT
    offre_id
    , intitule_offre
    , description_offre
    , liste_mots_cles
FROM
    descriptionoffre
WHERE
    metier_data IN ('DA' , 'DE' , 'DS')
