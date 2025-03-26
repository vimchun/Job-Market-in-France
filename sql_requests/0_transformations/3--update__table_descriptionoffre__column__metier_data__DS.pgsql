-- Code pour afficher les offres DS
-- SELECT DISTINCT
--     offre_id
--     , intitule_offre
-- FROM
--     descriptionoffre
------------
-- Code pour mettre à jour les offres DS (attribut "metier_data")
UPDATE
    descriptionoffre
SET
    "metier_data" = 'DS' -- écrit dans la colonne
    --     ------------
WHERE
    -- inclusion
    (intitule_offre ILIKE '%data%scientist%' -- "Data-Scientist", "Datascientist"
        OR intitule_offre ILIKE '%data%science%' -- "Data-Science"
        OR intitule_offre ILIKE '%scientifique donnée%' -- "Scientifique des données"
)
    -- exlusion
    AND intitule_offre NOT ILIKE '%développeur%' -- "développeur big data"
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
