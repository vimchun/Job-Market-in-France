SELECT
    o.id_offre
    , o.intitule_offre
    , e.nom_entreprise
    , s.code_naf
    , m.code_rome
FROM
    offresemploi o
    JOIN offre_entreprise oe ON o.id_offre = oe.id_offre
    JOIN entreprises e ON e.nom_entreprise = oe.nom_entreprise
    JOIN offre_secteur os ON o.id_offre = os.id_offre
    JOIN secteurs s ON s.code_naf = os.code_naf
    JOIN offre_metier om ON o.id_offre = om.id_offre
    JOIN metiers m ON om.code_rome = m.code_rome
LIMIT 1000;

