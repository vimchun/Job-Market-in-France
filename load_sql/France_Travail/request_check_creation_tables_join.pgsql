SELECT
    oe.offre_id
    , oc.competence_id
    , c.competence_code
    , c.competence_libelle
    , c.competence_code_exigence
FROM
    OffreEmploi oe
    JOIN Offre_Competence oc ON oe.offre_id = oc.offre_id
    JOIN Competence c ON oc.competence_id = c.competence_id
LIMIT 100;