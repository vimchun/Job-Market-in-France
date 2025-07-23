-- Requête 1 pour retourner le nombre total d'offres factices
SELECT
    COUNT(*) AS "total offres factice"
FROM (
    SELECT
        ofe.offre_id AS offre
    FROM
        offreemploi ofe
        JOIN descriptionoffre dof ON ofe.offre_id = dof.offre_id
    WHERE
        intitule_offre = 'Offre factice pour FastAPI');

-- SEPARATEUR POUR FASTAPI
-- Requête 2 pour retourner la liste des offres factices
SELECT
    ofe.offre_id AS offre
FROM
    offreemploi ofe
    JOIN descriptionoffre dof ON ofe.offre_id = dof.offre_id
WHERE
    intitule_offre = 'Offre factice pour FastAPI'