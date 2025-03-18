-- Code pour afficher les offres DA
-- SELECT DISTINCT
--     offre_id
--     , intitule_offre
-- FROM
--     descriptionoffre
------------
-- Code pour mettre à jour les offres DA (attribut "metier_data")
UPDATE
    descriptionoffre
SET
    "metier_data" = 'DA' -- écrit dans la colonne
    ------------
WHERE
    -- inclusion
    (intitule_offre ILIKE '%data%'
        OR intitule_offre ILIKE '%données%')
    AND (intitule_offre ILIKE '%analys%' -- "analyst" ou "analyste"
        OR intitule_offre ILIKE '%viz%' -- "vizualisation" ou "viz"
        OR intitule_offre ILIKE '%vis%'
        OR intitule_offre ILIKE '%power bi%') -- "visualisation"
    -- exlusion
    -- AND intitule_offre NOT ILIKE '%scien%' -- "data scientist" ou "data science"
    -- AND intitule_offre NOT ILIKE '%développeur%' -- "développeur big data"
    AND intitule_offre NOT ILIKE '%center%' -- "data center"
    AND intitule_offre NOT ILIKE '%software%' -- "ingénieur software"
    AND intitule_offre NOT ILIKE '%base%' -- "ingénieur base de données
    AND intitule_offre NOT ILIKE '%réseau%' -- "Ingénieur Système, réseaux, données"
    AND intitule_offre NOT ILIKE '%observabilité%' -- "Ingénieur Observabilité (Dynatrace/Datadog)"
    AND intitule_offre NOT ILIKE '%logiciel%' -- "Ingénieur Logiciel"
    AND intitule_offre NOT ILIKE '%analytics%' -- "Data Analytics"
    AND intitule_offre NOT ILIKE '%chef%' -- "Chef De Projet"
    AND intitule_offre NOT ILIKE '%business%' -- "business analyst"
    AND intitule_offre NOT ILIKE '%cyber%' -- "cybersécurité"
    AND intitule_offre NOT ILIKE '%sre%' -- "Site Reliability Engineer"
    AND intitule_offre NOT ILIKE '%marketing%' -- "data marketing"
    AND intitule_offre NOT ILIKE '%manager%'
    AND intitule_offre NOT ILIKE '%gouvernance%'
    AND intitule_offre NOT ILIKE '%audit%' -- "Analyste Audit IT"
    AND intitule_offre NOT ILIKE '%SOC%' -- "Security Operation Center"
    AND intitule_offre NOT ILIKE '%advisory%' -- "Data Advisory"
    AND intitule_offre NOT ILIKE '%supervision%' -- "Ingénieur supervision IT Datacenter
    AND intitule_offre NOT ILIKE '%responsable%'
    AND intitule_offre NOT ILIKE '%directeur%'
    AND intitule_offre NOT ILIKE '%formation%'
    AND intitule_offre NOT ILIKE '%certification%';

-- ILIKE : case insensitive


-- filtre_offres_DA:
--   - a_inclure:
--       - Analyste Décisionnel
--       - Data Analyst # le code récupérera par exemple : "Data-Analyst", "Analyste Data", "Analystes Data"...
--       - Analys Donnée # le code récupérera par exemple : "Analyse De Données", "Analyste De Données"...
--       - Data Vi(s|z) # le code récupérera par exemple : "DataViz", "DataVis", "Data Visualisation", "Data Vizualisation", "DataVisualisation"...
--       - Business Intelligence
--       - Power BI
--
--   - a_exclure: # chaque clé ne doit avoir qu'un mot (restriction liée à l'API d'Adzuna)
--       - Fonctionnel # exclut "Analyste Fonctionnel"
--       - Développeur # exclut "Analyste Développeur"
--       - Programmeur # exclut "Analyste Programmeur"
--       - SOC # exclut "Analyste SOC"
--       - Trésorerie # exclut "Analyste trésorerie"
--       - Cybersécurité # exclut "Analyste cybersécurité"
--       - Advisory # exclut Data Advisory
--       - Informaticien
--       - Chef
--       - Manager
--       - Responsable
--       - Directeur
--       - Formation
--       - Certification

