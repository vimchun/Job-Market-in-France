-- Voir la diagramme UML
--
--
CREATE TABLE OffresEmploi (
    id_offre VARCHAR(7) NOT NULL PRIMARY KEY
    , intitule_offre NOT NULL VARCHAR(100)
    , description_offre NOT NULL VARCHAR(5000)
    , date_creation DATE
    , date_actualisation DATE
    , nombre_postes INTEGER
    , nom_partenaire VARCHAR(30)
    , accessible_travailleurs_handicapes BOOLEAN
    , difficile_a_pourvoir BOOLEAN
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Entreprise (
    id_offre VARCHAR(7) NOT NULL
    , nom_entreprise VARCHAR(100) NOT NULL
    , PRIMARY KEY (id_offre , nom_entreprise)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (nom_entreprise) REFERENCES Entreprises (nom_entreprise)
);

CREATE TABLE Entreprises (
    nom_entreprise VARCHAR(100) NOT NULL PRIMARY KEY
    , entreprise_adaptee BOOLEAN
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Secteur (
    id_offre VARCHAR(7) NOT NULL
    , code_naf VARCHAR(6) NOT NULL
    , PRIMARY KEY (id_offre , code_naf)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_naf) REFERENCES Secteurs (code_naf)
);

CREATE TABLE Secteurs (
    code_naf VARCHAR(6) NOT NULL PRIMARY KEY
    , secteur_activite NOT NULL VARCHAR(50)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Metier (
    id_offre VARCHAR(7) NOT NULL
    , code_rome VARCHAR(5) NOT NULL
    , PRIMARY KEY (id_offre , code_rome)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_rome) REFERENCES Metiers (code_rome)
);

CREATE TABLE Metiers (
    code_rome VARCHAR(5) NOT NULL PRIMARY KEY
    , appellation_rome NOT NULL VARCHAR(50)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Experience (
    id_offre VARCHAR(7) NOT NULL
    , id_experience INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_experience)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_experience) REFERENCES Experiences (id_experience)
);

CREATE TABLE Experiences (
    id_experience SERIAL NOT NULL PRIMARY KEY
    , libelle_experience NOT NULL VARCHAR(20)
    , code_exigence_experience NOT NULL VARCHAR(1)
    , commentaire_experience VARCHAR(200)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Qualification (
    id_offre VARCHAR(7) NOT NULL
    , code_qualification VARCHAR(1) NOT NULL
    , PRIMARY KEY (id_offre , code_qualification)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_qualification) REFERENCES Qualifications (code_qualification)
);

CREATE TABLE Qualifications (
    code_qualification VARCHAR(1) NOT NULL PRIMARY KEY
    , libelle_qualification NOT NULL VARCHAR(20)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Formation (
    id_offre VARCHAR(7) NOT NULL
    , id_formation INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_formation)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_formation) REFERENCES Formations (id_formation)
);

CREATE TABLE Formations (
    id_formation SERIAL NOT NULL PRIMARY KEY
    , code_formation NOT NULL VARCHAR(5)
    , libelle_niveau_formation NOT NULL VARCHAR(30)
    , libelle_domaine_formation NOT NULL VARCHAR(30)
    , code_exigence_formation NOT NULL VARCHAR(1)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Competence (
    id_offre VARCHAR(7) NOT NULL
    , id_competence INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_competence)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_competence) REFERENCES Competences (id_competence)
);

CREATE TABLE Competences (
    id_competence SERIAL NOT NULL PRIMARY KEY
    , code_competence NOT NULL VARCHAR(6)
    , libelle_competence NOT NULL VARCHAR(100)
    , code_exigence_competence NOT NULL VARCHAR(1)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_QualitePro (
    id_offre VARCHAR(7) NOT NULL
    , libelle_qualite_pro VARCHAR(100) NOT NULL
    , PRIMARY KEY (id_offre , libelle_qualite_pro)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (libelle_qualite_pro) REFERENCES QualitesProfessionnelles (libelle_qualite_pro)
);

CREATE TABLE QualitesProfessionnelles (
    libelle_qualite_pro VARCHAR(100) NOT NULL PRIMARY KEY
    , description_qualite_pro NOT NULL VARCHAR(1000)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_Langue (
    id_offre VARCHAR(7) NOT NULL
    , id_langue INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_offre)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_offre) REFERENCES Langues (id_offre)
);

CREATE TABLE Langues (
    id_langue SERIAL NOT NULL PRIMARY KEY
    , libelle_langue NOT NULL VARCHAR(30)
    , code_exigence_langue NOT NULL VARCHAR(1)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Offre_PermisConduire (
    id_offre VARCHAR(7) NOT NULL
    , id_permis_conduire INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_permis_conduire)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_permis_conduire) REFERENCES PermisConduire (id_permis_conduire)
);

CREATE TABLE PermisConduire (
    id_permis_conduire SERIAL NOT NULL PRIMARY KEY
    , libelle_permis NOT NULL VARCHAR(20)
    , code_exigence_permis NOT NULL VARCHAR(1)
);

----------------------------------------------------------------
CREATE TABLE LieuxTravail (
    id_lieu_travail SERIAL NOT NULL PRIMARY KEY
    , libelle_lieu_travail NOT NULL VARCHAR(30)
    , code_commune NOT NULL VARCHAR(5)
    , latitude FLOAT
    , longitude FLOAT
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE LieuTravail_Ville (
    id_offre VARCHAR(7) NOT NULL
    , code_postal VARCHAR(5) NOT NULL
    , PRIMARY KEY (id_offre , code_postal)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (code_postal) REFERENCES Villes (code_postal)
);

CREATE TABLE Villes (
    code_postal VARCHAR(5) SERIAL NOT NULL PRIMARY KEY
    , dpt_ville_arrdt NOT NULL VARCHAR(50)
);

----------------------------------------------------------------
CREATE TABLE Contrats (
    id_contrat SERIAL NOT NULL PRIMARY KEY
    , code_type_contrat NOT NULL VARCHAR(10)
    , libelle_type_contrat VARCHAR(30)
    , nature_contrat VARCHAR(30)
    , temps_travail VARCHAR(100)
    , condition_exercice VARCHAR(50)
    , alternance BOOLEAN
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Contrat_DureeTravail (
    id_offre VARCHAR(7) NOT NULL
    , id_duree_travail INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_duree_travail)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_duree_travail) REFERENCES DureeTravail (id_duree_travail)
);

CREATE TABLE DureeTravail (
    id_duree_travail SERIAL NOT NULL PRIMARY KEY
    , libelle_duree_travail NOT NULL VARCHAR(20)
    , libelle_duree_travail_converti VARCHAR(20)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Contrat_Salaire (
    id_offre VARCHAR(7) NOT NULL
    , id_salaire INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_salaire)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_salaire) REFERENCES Salaire (id_salaire)
);

CREATE TABLE Salaire (
    id_salaire SERIAL NOT NULL PRIMARY KEY
    , libelle_salaire NOT NULL VARCHAR(50)
    , complement_au_salaire_1 VARCHAR(30)
    , complement_au_salaire_2 VARCHAR(30)
    , commentaire_salaire VARCHAR(30)
);

----------------------------------------------------------------
-- table de liaison
CREATE TABLE Contrat_Deplacement (
    id_offre VARCHAR(7) NOT NULL
    , id_deplacement INTEGER NOT NULL
    , PRIMARY KEY (id_offre , id_deplacement)
    , FOREIGN KEY (id_offre) REFERENCES OffresEmploi (id_offre)
    , FOREIGN KEY (id_deplacement) REFERENCES Deplacements (id_deplacement)
);

CREATE TABLE Deplacements (
    id_deplacement SERIAL NOT NULL PRIMARY KEY
    , code_deplacement NOT NULL VARCHAR(1)
    , libelle_deplacement NOT NULL VARCHAR(30)
);

