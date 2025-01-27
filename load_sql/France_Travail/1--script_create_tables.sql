-- Voir la diagramme UML
--
--
CREATE TABLE OffresEmploi (
    id_offre VARCHAR(10) NOT NULL PRIMARY KEY
    , intitule_offre VARCHAR(200) NOT NULL
    , description_offre VARCHAR(5000) NOT NULL
    , date_creation DATE
    , date_actualisation DATE
    , nombre_postes INTEGER
    , nom_partenaire VARCHAR(30)
    , accessible_travailleurs_handicapes BOOLEAN
    , difficile_a_pourvoir BOOLEAN
);

----------------------------------------------------------------
CREATE TABLE Entreprises (
    nom_entreprise VARCHAR(100) PRIMARY KEY NOT NULL
    , entreprise_adaptee BOOLEAN
);

-- table de liaison
CREATE TABLE Offre_Entreprise (
    id_offre VARCHAR(7) NOT NULL
    , nom_entreprise VARCHAR(100) NOT NULL
    , PRIMARY KEY (id_offre , nom_entreprise)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (nom_entreprise) REFERENCES Entreprises (nom_entreprise)
);

----------------------------------------------------------------
CREATE TABLE Secteurs (
    code_naf VARCHAR(6) PRIMARY KEY NOT NULL
    , secteur_activite VARCHAR(200) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Secteur (
    id_offre VARCHAR(7) NOT NULL
    , code_naf VARCHAR(6) NOT NULL
    , PRIMARY KEY (id_offre , code_naf)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_naf) REFERENCES Secteurs (code_naf)
);

----------------------------------------------------------------
CREATE TABLE Metiers (
    code_rome VARCHAR(5) PRIMARY KEY NOT NULL
    , appellation_rome VARCHAR(100) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Metier (
    id_offre VARCHAR(7) NOT NULL
    , code_rome VARCHAR(5) NOT NULL
    , PRIMARY KEY (id_offre , code_rome)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_rome) REFERENCES Metiers (code_rome)
);

----------------------------------------------------------------
CREATE TABLE Experiences (
    id_experience SERIAL NOT NULL PRIMARY KEY
    , libelle_experience VARCHAR(100) NOT NULL
    , code_exigence_experience VARCHAR(1) NOT NULL
    , commentaire_experience VARCHAR(200)
    , CONSTRAINT unique_experience UNIQUE (libelle_experience , code_exigence_experience)
);

-- table de liaison
CREATE TABLE Offre_Experience (
    id_offre VARCHAR(7) NOT NULL
    , id_experience INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_experience)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_experience) REFERENCES Experiences (id_experience)
);

----------------------------------------------------------------
CREATE TABLE Qualifications (
    code_qualification VARCHAR(1) PRIMARY KEY NOT NULL
    , libelle_qualification VARCHAR(20) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Qualification (
    id_offre VARCHAR(7) NOT NULL
    , code_qualification VARCHAR(1) NOT NULL
    , PRIMARY KEY (id_offre , code_qualification)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_qualification) REFERENCES Qualifications (code_qualification)
);

----------------------------------------------------------------
CREATE TABLE Formations (
    id_formation SERIAL NOT NULL PRIMARY KEY
    , code_formation VARCHAR(5) NOT NULL
    , libelle_niveau_formation VARCHAR(30) NOT NULL
    , libelle_domaine_formation VARCHAR(30) NOT NULL
    , code_exigence_formation VARCHAR(1) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Formation (
    id_offre VARCHAR(7) NOT NULL
    , id_formation INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_formation)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_formation) REFERENCES Formations (id_formation)
);

----------------------------------------------------------------
CREATE TABLE Competences (
    id_competence SERIAL NOT NULL PRIMARY KEY
    , code_competence VARCHAR(6) NOT NULL
    , libelle_competence VARCHAR(100) NOT NULL
    , code_exigence_competence VARCHAR(1) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Competence (
    id_offre VARCHAR(7) NOT NULL
    , id_competence INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_competence)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_competence) REFERENCES Competences (id_competence)
);

----------------------------------------------------------------
CREATE TABLE QualitesProfessionnelles (
    libelle_qualite_pro VARCHAR(100) NOT NULL PRIMARY KEY
    , description_qualite_pro VARCHAR(1000) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_QualitePro (
    id_offre VARCHAR(7) NOT NULL
    , libelle_qualite_pro VARCHAR(100) NOT NULL
    , PRIMARY KEY (id_offre , libelle_qualite_pro)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (libelle_qualite_pro) REFERENCES QualitesProfessionnelles (libelle_qualite_pro)
);

----------------------------------------------------------------
CREATE TABLE Langues (
    id_langue SERIAL NOT NULL PRIMARY KEY
    , libelle_langue VARCHAR(30) NOT NULL
    , code_exigence_langue VARCHAR(1) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_Langue (
    id_offre VARCHAR(7) NOT NULL
    , id_langue INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_langue)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_langue) REFERENCES Langues (id_langue)
);

----------------------------------------------------------------
CREATE TABLE PermisConduire (
    id_permis_conduire SERIAL NOT NULL PRIMARY KEY
    , libelle_permis VARCHAR(20) NOT NULL
    , code_exigence_permis VARCHAR(1) NOT NULL
);

-- table de liaison
CREATE TABLE Offre_PermisConduire (
    id_offre VARCHAR(7) NOT NULL
    , id_permis_conduire INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_permis_conduire)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_permis_conduire) REFERENCES PermisConduire (id_permis_conduire)
);

----------------------------------------------------------------
CREATE TABLE LieuxTravail (
    id_lieu_travail SERIAL NOT NULL PRIMARY KEY
    , libelle_lieu_travail VARCHAR(30) NOT NULL
    , code_commune VARCHAR(5) NOT NULL
    , latitude FLOAT
    , longitude FLOAT
);

----------------------------------------------------------------
CREATE TABLE Villes (
    code_postal VARCHAR(5) NOT NULL PRIMARY KEY
    , dpt_ville_arrdt VARCHAR(50) NOT NULL
);

-- table de liaison
CREATE TABLE LieuTravail_Ville (
    id_offre VARCHAR(7) NOT NULL
    , code_postal VARCHAR(5) NOT NULL
    , PRIMARY KEY (id_offre , code_postal)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_postal) REFERENCES Villes (code_postal)
);

----------------------------------------------------------------
CREATE TABLE Contrats (
    id_contrat SERIAL NOT NULL PRIMARY KEY
    , code_type_contrat VARCHAR(10) NOT NULL
    , libelle_type_contrat VARCHAR(30)
    , nature_contrat VARCHAR(30)
    , temps_travail VARCHAR(100)
    , condition_exercice VARCHAR(50)
    , alternance BOOLEAN
);

----------------------------------------------------------------
CREATE TABLE DureeTravail (
    id_duree_travail SERIAL NOT NULL PRIMARY KEY
    , libelle_duree_travail VARCHAR(20) NOT NULL
    , libelle_duree_travail_converti VARCHAR(20)
);

-- table de liaison
CREATE TABLE Contrat_DureeTravail (
    id_offre VARCHAR(7) NOT NULL
    , id_duree_travail INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_duree_travail)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_duree_travail) REFERENCES DureeTravail (id_duree_travail)
);

----------------------------------------------------------------
CREATE TABLE Salaire (
    id_salaire SERIAL NOT NULL PRIMARY KEY
    , libelle_salaire VARCHAR(50) NOT NULL
    , complement_au_salaire_1 VARCHAR(30)
    , complement_au_salaire_2 VARCHAR(30)
    , commentaire_salaire VARCHAR(30)
);

-- table de liaison
CREATE TABLE Contrat_Salaire (
    id_offre VARCHAR(7) NOT NULL
    , id_salaire INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_salaire)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_salaire) REFERENCES Salaire (id_salaire)
);

----------------------------------------------------------------
CREATE TABLE Deplacements (
    id_deplacement SERIAL NOT NULL PRIMARY KEY
    , code_deplacement VARCHAR(1) NOT NULL
    , libelle_deplacement VARCHAR(30) NOT NULL
);

-- table de liaison
CREATE TABLE Contrat_Deplacement (
    id_offre VARCHAR(7) NOT NULL
    , id_deplacement INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_deplacement)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_deplacement) REFERENCES Deplacements (id_deplacement)
);

