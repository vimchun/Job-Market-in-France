-------------------
-- table de fait --
-------------------
CREATE TABLE OffreEmploi (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , date_creation DATE
    , date_actualisation DATE
    , nombre_postes INTEGER
);

--------------------------
-- tables de dimension  --
--------------------------
CREATE TABLE Contrat (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , type_contrat VARCHAR(10)
    , type_contrat_libelle VARCHAR(30)
    , duree_travail_libelle VARCHAR(20)
    , duree_travail_libelle_converti VARCHAR(20)
    , nature_contrat VARCHAR(30)
    , salaire_commentaire VARCHAR(30)
    , salaire_libelle VARCHAR(50)
    , salaire_complement_1 VARCHAR(30)
    , salaire_complement_2 VARCHAR(30)
    , alternance BOOLEAN
    , deplacement_code VARCHAR(1)
    , deplacement_libelle VARCHAR(30)
    , temps_travail VARCHAR(100)
    , condition_specifique VARCHAR(50)
);

CREATE TABLE Entreprise (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , nom_entreprise VARCHAR(100)
    , description_entreprise VARCHAR(100)
    , entreprise_adaptee BOOLEAN
    , code_naf VARCHAR(6)
    , secteur_activite_libelle VARCHAR(200)
);

CREATE TABLE Localisation (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , description_lieu VARCHAR(50)
    , code_postal VARCHAR(5)
    , code_commune VARCHAR(5)
);

CREATE TABLE DescriptionOffre (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , intitule_offre VARCHAR(200)
    , description_offre VARCHAR(5000)
    , nom_partenaire VARCHAR(30)
    , rome_code VARCHAR(5)
    , rome_libelle VARCHAR(50)
    , appellation_rome VARCHAR(100)
    , difficile_a_pourvoir BOOLEAN
    , accessible_travailleurs_handicapes BOOLEAN
);

----------------------------------------------
-- tables de dimension et tables de liaison --
----------------------------------------------
CREATE TABLE Competence (
    competence_id SERIAL NOT NULL PRIMARY KEY
    , competence_code VARCHAR(6) NOT NULL
    , competence_libelle VARCHAR(100) NOT NULL
    , competence_code_exigence VARCHAR(1) NOT NULL
);

CREATE TABLE Offre_Competence (
    offre_id VARCHAR(7) NOT NULL
    , competence_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , competence_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (competence_id) REFERENCES Competence (competence_id)
);

CREATE TABLE Experience (
    experience_id SERIAL NOT NULL PRIMARY KEY
    , experience_libelle VARCHAR(100) NOT NULL
    , experience_code_exigence VARCHAR(1) NOT NULL
    , experience_commentaire VARCHAR(200)
    , CONSTRAINT unique_experience UNIQUE (experience_libelle , experience_code_exigence)
);

CREATE TABLE Offre_Experience (
    offre_id VARCHAR(7) NOT NULL
    , experience_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , experience_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (experience_id) REFERENCES Experience (experience_id)
);

CREATE TABLE NiveauFormation (
    niveau_formation_id SERIAL NOT NULL PRIMARY KEY
    , niveau_formation_libelle VARCHAR(30) NOT NULL
    , niveau_formation_code_exigence VARCHAR(1) NOT NULL
);

CREATE TABLE Offre_NiveauFormation (
    offre_id VARCHAR(7) NOT NULL
    , niveau_formation_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , niveau_formation_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (niveau_formation_id) REFERENCES NiveauFormation (niveau_formation_id)
);

CREATE TABLE DomaineFormation (
    domaine_formation_code INTEGER NOT NULL PRIMARY KEY
    , domaine_formation_libelle VARCHAR(30) NOT NULL
);

CREATE TABLE Offre_DomaineFormation (
    offre_id VARCHAR(7) NOT NULL
    , domaine_formation_code INTEGER NOT NULL
    , PRIMARY KEY (offre_id , domaine_formation_code)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (domaine_formation_code) REFERENCES DomaineFormation (domaine_formation_code)
);

CREATE TABLE QualiteProfessionnelle (
    qualite_professionnelle_id SERIAL NOT NULL PRIMARY KEY
    , qualite_professionnelle_libelle VARCHAR(100) NOT NULL
    , qualite_professionnelle_description VARCHAR(1000) NOT NULL
);

CREATE TABLE Offre_QualiteProfessionnelle (
    offre_id VARCHAR(7) NOT NULL
    , qualite_professionnelle_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , qualite_professionnelle_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (qualite_professionnelle_id) REFERENCES QualiteProfessionnelle (qualite_professionnelle_id)
);

CREATE TABLE Qualification (
    qualification_code VARCHAR(1) PRIMARY KEY NOT NULL
    , qualification_libelle VARCHAR(20) NOT NULL
);

CREATE TABLE Offre_Qualification (
    offre_id VARCHAR(7) NOT NULL
    , qualification_code VARCHAR(1) NOT NULL
    , PRIMARY KEY (offre_id , qualification_code)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (qualification_code) REFERENCES Qualification (qualification_code)
);

CREATE TABLE Langue (
    langue_id SERIAL NOT NULL PRIMARY KEY
    , langue_libelle VARCHAR(30) NOT NULL
    , langue_code_exigence VARCHAR(1) NOT NULL
);

CREATE TABLE Offre_Langue (
    offre_id VARCHAR(7) NOT NULL
    , langue_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , langue_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (langue_id) REFERENCES Langue (langue_id)
);

CREATE TABLE PermisConduire (
    permis_id SERIAL NOT NULL PRIMARY KEY
    , permis_libelle VARCHAR(20) NOT NULL
    , permis_code_exigence VARCHAR(1) NOT NULL
);

CREATE TABLE Offre_PermisConduire (
    offre_id VARCHAR(7) NOT NULL
    , permis_id INTEGER NOT NULL
    , PRIMARY KEY (offre_id , permis_id)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id)
    , FOREIGN KEY (permis_id) REFERENCES PermisConduire (permis_id)
);