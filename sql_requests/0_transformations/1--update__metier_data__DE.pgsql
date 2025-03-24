-- Code pour afficher les offres DE
-- SELECT DISTINCT
--     offre_id
--     , intitule_offre
-- FROM
--     descriptionoffre
------------
-- Code pour mettre à jour les offres DE (attribut "metier_data")
UPDATE
    descriptionoffre
SET
    "metier_data" = 'DE' -- écrit dans la colonne
    ------------
WHERE
    -- inclusion
    (intitule_offre ILIKE '%ing%' -- ingénieur
        OR intitule_offre ILIKE '%eng%') -- engineer
    AND (intitule_offre ILIKE '%data%'
        OR intitule_offre ILIKE '%données%')
    -- exlusion
    AND intitule_offre NOT ILIKE '%visuali%' -- "data visualisation" ou "data visualization"
    AND intitule_offre NOT ILIKE '%viz%' -- "data viz"
    AND intitule_offre NOT ILIKE '%scien%' -- "data scientist" ou "data science"
    AND intitule_offre NOT ILIKE '%center%' -- "data center"
    -- AND intitule_offre NOT ILIKE '%développeur%' -- "développeur big data"
    AND intitule_offre NOT ILIKE '%software%' -- "ingénieur software"
    AND intitule_offre NOT ILIKE '%architect%' -- "architecte data"
    AND intitule_offre NOT ILIKE '%base%' -- "ingénieur base de données
    AND intitule_offre NOT ILIKE '%réseau%' -- "Ingénieur Système, réseaux, données"
    AND intitule_offre NOT ILIKE '%model%' -- "Data Modeling"
    AND intitule_offre NOT ILIKE '%observabilité%' -- "Ingénieur Observabilité (Dynatrace/Datadog)"
    AND intitule_offre NOT ILIKE '%logiciel%' -- "Ingénieur Logiciel"
    AND intitule_offre NOT ILIKE '%analys%' -- "Data Analyst" ou "analyse de données"
    AND intitule_offre NOT ILIKE '%analytics%' -- "Data Analytics"
    AND intitule_offre NOT ILIKE '%chef%' -- "Chef De Projet"
    AND intitule_offre NOT ILIKE '%business%' -- "business analyst"
    AND intitule_offre NOT ILIKE '%cyber%' -- "cybersécurité"
    AND intitule_offre NOT ILIKE '%sre%' -- "Site Reliability Engineer"
    AND intitule_offre NOT ILIKE '%marketing%' -- "data marketing"
    AND intitule_offre NOT ILIKE '%manager%'
    AND intitule_offre NOT ILIKE '%gouvernance%'
    AND intitule_offre NOT ILIKE '%responsable%'
    AND intitule_offre NOT ILIKE '%directeur%'
    AND intitule_offre NOT ILIKE '%formation%'
    AND intitule_offre NOT ILIKE '%certification%';
    -- ILIKE : case insensitive
