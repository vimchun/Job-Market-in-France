-- Code pour afficher les offres DA
-- SELECT DISTINCT
--     offre_id
--     , intitule_offre
-- FROM
--     descriptionoffre
------------
-- Code pour mettre à jour les offres DA (attribut "metier_data")
ALTER TABLE descriptionoffre
    ADD COLUMN IF NOT EXISTS metier_data VARCHAR(2);

UPDATE
    descriptionoffre
SET
    metier_data = 'DA' -- écrit dans la colonne
    ------------
WHERE
    -- inclusion
    (intitule_offre ILIKE '%data%'
        OR intitule_offre ILIKE '%données%')
    AND (intitule_offre ILIKE '%analys%' -- "analyst" ou "analyste"
        OR intitule_offre ILIKE '%viz%' -- "vizualisation" ou "viz"
        OR intitule_offre ILIKE '%vis%'
        OR intitule_offre ILIKE '%power%bi%'
        OR intitule_offre ILIKE '%business%intelligence%') -- "visualisation"
    -- exclusion
    -- AND intitule_offre NOT ILIKE '%scien%' -- "data scientist" ou "data science"
    AND intitule_offre NOT ILIKE '%développeur%' -- "Analyste Développeur"
    AND intitule_offre NOT ILIKE '%programmeur%' -- "Analyste Programmeur"
    AND intitule_offre NOT ILIKE '%informaticien%'
    AND intitule_offre NOT ILIKE '%center%' -- "data center"
    AND intitule_offre NOT ILIKE '%software%' -- "ingénieur software"
    AND intitule_offre NOT ILIKE '%base%' -- "ingénieur base de données
    AND intitule_offre NOT ILIKE '%réseau%' -- "Ingénieur Système, réseaux, données"
    AND intitule_offre NOT ILIKE '%observabilité%' -- "Ingénieur Observabilité (Dynatrace/Datadog)"
    AND intitule_offre NOT ILIKE '%logiciel%' -- "Ingénieur Logiciel"
    AND intitule_offre NOT ILIKE '%analytics%' -- "Data Analytics"
    AND intitule_offre NOT ILIKE '%chef%' -- "Chef De Projet"
    AND intitule_offre NOT ILIKE '%cyber%' -- "cybersécurité"
    AND intitule_offre NOT ILIKE '%sre%' -- "Site Reliability Engineer"
    AND intitule_offre NOT ILIKE '%marketing%' -- "data marketing"
    AND intitule_offre NOT ILIKE '%manager%'
    AND intitule_offre NOT ILIKE '%gouvernance%'
    AND intitule_offre NOT ILIKE '%audit%' -- "Analyste Audit IT"
    AND intitule_offre NOT ILIKE '%SOC%' -- "Analyste SOC" (Security Operation Center)
    AND intitule_offre NOT ILIKE '%advisory%' -- "Data Advisory"
    AND intitule_offre NOT ILIKE '%supervision%' -- "Ingénieur supervision IT Datacenter
    AND intitule_offre NOT ILIKE '%responsable%'
    AND intitule_offre NOT ILIKE '%directeur%'
    AND intitule_offre NOT ILIKE '%formation%'
    AND intitule_offre NOT ILIKE '%certification%'
    AND intitule_offre NOT ILIKE '%trésorerie%' -- "Analyste trésorerie"
    AND intitule_offre NOT ILIKE '%fonctionnel%' --"Analyste Fonctionnel"
;

-- ILIKE : case insensitive
