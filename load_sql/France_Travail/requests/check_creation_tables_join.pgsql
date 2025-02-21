SELECT
    oe.offre_id
    , oc.competence_id
    , c.competence_code
    , c.competence_libelle
    , c.competence_code_exigence
    -- , nf.niveau_formation_id
    -- , nf.niveau_formation_libelle
    -- , nf.niveau_formation_code_exigence
    -- , df.domaine_formation_code
    -- , df.domaine_formation_libelle
FROM
    OffreEmploi oe
    JOIN Offre_Competence oc ON oe.offre_id = oc.offre_id
    JOIN Competence c ON oc.competence_id = c.competence_id
    -- JOIN OFfre_NiveauFormation onf ON oe.offre_id = onf.offre_id
    -- JOIN NiveauFormation nf ON nf.niveau_formation_id = onf.niveau_formation_id
    -- JOIN Offre_DomaineFormation odf ON oe.offre_id = odf.offre_id
    -- JOIN DomaineFormation df ON df.domaine_formation_code = odf.domaine_formation_code
WHERE
    oe.offre_id = '186NWKN';
    -- oe.offre_id = '149VCXW';
-- LIMIT 100;
;

