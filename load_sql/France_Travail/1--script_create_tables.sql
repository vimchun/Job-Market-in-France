-- D'après notre fichier csv, les tables se déclinent de cette manière :
--
-- code_ROME (`romeCode`)
-- contrat (`typeContrat`, `typeContratLibelle`, `natureContrat`, `dureeTravailLibelleConverti`, `alternance`)
-- date (`dateCreation`, `dateActualisation`)
-- entreprise (`entreprise` > `nom`, `entreprise` > `entrepriseAdaptee`)
-- exigences (`experienceExige`, `experienceLibelle`, `formations` > `niveauLiBelle`, `formations` > `exigence`, `qualitesProfessionnelles` (liste) > `libelle`, `qualitesProfessionnelles` (liste) > `description`)
-- exigences_compétences (`competences` >  `code`, `competences` >  `libelle`, `competences` >  `exigence`, `experienceCommentaire`)
-- origine (`origineOffre` > `origine`, `origineOffre` > `partenaires` (si origine:2), `origineOffre` > `partenaires`> `nom`)
-- salaire (`salaire` > `libelle`, `salaire` > `complement1`)
-- secteur (`codeNAF`, `secteurActivite`, `secteurActiviteLibelle`)
-- offre (`id`, `intitule`, `description`, `nombrePostes`, `accessibleTH`, `deplacementLibelle`, `qualificationLibelle`, `offresManqueCandidats`, `complementExercice`)

DROP TABLE IF EXISTS offre;

CREATE TABLE offre (
    id VARCHAR(20) PRIMARY KEY
    , intitule VARCHAR(1000)
    , description VARCHAR(10000)
    , nombrePostes INT
    , accessibleTH BOOLEAN
    , deplacementLibelle VARCHAR(100)
    , qualificationLibelle VARCHAR(200)
    , offresManqueCandidats BOOLEAN
    , complementExercice VARCHAR(100)
);

DROP TABLE IF EXISTS localisation;

CREATE TABLE localisation (
    id VARCHAR(20) PRIMARY KEY
    , latitude FLOAT
    , longitude FLOAT
    , codePostal INT
);
