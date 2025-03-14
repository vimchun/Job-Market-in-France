-- -- script pour supprimer toutes les tables pour revenir sur une bdd vierge
-- DROP TABLE OffreEmploi;

-- DROP TABLE Contrat;

-- DROP TABLE Entreprise;

-- DROP TABLE Localisation;

-- DROP TABLE DescriptionOffre;

-- DROP TABLE Competence;

-- DROP TABLE Experience;

-- DROP TABLE Formation;

-- DROP TABLE QualiteProfessionnelle;

-- DROP TABLE Qualification;

-- DROP TABLE Langue;

-- DROP TABLE PermisConduire;

-- DROP TABLE Offre_Competence;

-- DROP TABLE Offre_Experience;

-- DROP TABLE Offre_Formation;

-- DROP TABLE Offre_QualiteProfessionnelle;

-- DROP TABLE Offre_Qualification;

-- DROP TABLE Offre_Langue;

-- DROP TABLE Offre_PermisConduire;

-- Suppression avec CASCADE pour prendre en compte les clés étrangères
DROP TABLE IF EXISTS
    Offre_Competence,
    Offre_Experience,
    Offre_Formation,
    Offre_QualiteProfessionnelle,
    Offre_Qualification,
    Offre_Langue,
    Offre_PermisConduire,
    PermisConduire,
    Langue,
    Qualification,
    QualiteProfessionnelle,
    Formation,
    Experience,
    Competence,
    Localisation,
    DescriptionOffre,
    Entreprise,
    Contrat,
    OffreEmploi CASCADE;
