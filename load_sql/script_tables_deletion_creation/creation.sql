-------------------
-- table de fait --
-------------------
-- DROP TABLE OffreEmploi CASCADE;
CREATE TABLE OffreEmploi (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , date_extraction DATE
    , date_premiere_ecriture DATE
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
    , type_contrat_libelle VARCHAR(100)
    , duree_travail_libelle VARCHAR(100)
    , duree_travail_libelle_converti VARCHAR(100)
    , nature_contrat VARCHAR(100)
    , salaire_libelle VARCHAR(100)
    , salaire_complement_1 VARCHAR(100)
    , salaire_complement_2 VARCHAR(100)
    , salaire_commentaire VARCHAR(100)
    , alternance BOOLEAN
    , deplacement_code INTEGER
    , deplacement_libelle VARCHAR(100)
    , temps_travail VARCHAR(100)
    , condition_specifique VARCHAR(100)
);

CREATE TABLE Entreprise (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , nom_entreprise VARCHAR(100)
    , description_entreprise VARCHAR(1000)
    , entreprise_adaptee BOOLEAN
    , code_naf VARCHAR(6)
    , secteur_activite_libelle VARCHAR(200)
);

-- DROP TABLE Localisation;
CREATE TABLE Localisation (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , code_insee VARCHAR(5)
    , nom_commune VARCHAR(200)
    , code_postal VARCHAR(5)
    , nom_ville VARCHAR(200)
    , code_departement VARCHAR(3)
    , nom_departement VARCHAR(200)
    , code_region VARCHAR(2)
    , nom_region VARCHAR(200)
);

-- DROP TABLE DescriptionOffre CASCADE;
CREATE TABLE DescriptionOffre (
    offre_id VARCHAR(7) NOT NULL PRIMARY KEY
    , intitule_offre VARCHAR(200)
    , description_offre VARCHAR(5000)
    , nom_partenaire VARCHAR(30)
    , rome_code VARCHAR(5)
    , rome_libelle VARCHAR(100)
    , appellation_rome VARCHAR(100)
    , difficile_a_pourvoir BOOLEAN
    , accessible_travailleurs_handicapes BOOLEAN
);

----------------------------------------------
-- tables de dimension et tables de liaison --
----------------------------------------------
-- note: ON DELETE CASCADE pour maintenir l'intégrité des données :
--  pour supprimer toutes les lignes associées dans Offre_Competence si une offre ou une compétence correspondante est supprimée
-- DROP TABLE Competence CASCADE;
CREATE TABLE Competence (
    competence_id SERIAL NOT NULL PRIMARY KEY
    , competence_code INTEGER
    , competence_libelle VARCHAR(500)
    , competence_code_exigence VARCHAR(1)
    , CONSTRAINT competence_unique UNIQUE (competence_code , competence_libelle , competence_code_exigence)
);

-- DROP TABLE Offre_Competence CASCADE;
CREATE TABLE Offre_Competence (
    offre_id VARCHAR(7) NOT NULL
    , competence_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , competence_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (competence_id) REFERENCES Competence (competence_id) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE Experience CASCADE;
CREATE TABLE Experience (
    experience_id SERIAL NOT NULL PRIMARY KEY
    , experience_libelle VARCHAR(100)
    , experience_code_exigence VARCHAR(1)
    , experience_commentaire VARCHAR(200)
    , CONSTRAINT experience_unique UNIQUE (experience_libelle , experience_code_exigence , experience_commentaire)
);

-- DROP TABLE Offre_Experience CASCADE;
CREATE TABLE Offre_Experience (
    offre_id VARCHAR(7) NOT NULL
    , experience_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , experience_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (experience_id) REFERENCES Experience (experience_id) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE Formation CASCADE;
CREATE TABLE Formation (
    formation_id SERIAL NOT NULL PRIMARY KEY
    , formation_code INTEGER
    , formation_domaine_libelle VARCHAR(100)
    , formation_niveau_libelle VARCHAR(30)
    , formation_commentaire VARCHAR(100)
    , formation_code_exigence VARCHAR(1)
    , CONSTRAINT formation_unique UNIQUE (formation_code , formation_domaine_libelle , formation_niveau_libelle , formation_commentaire , formation_code_exigence)
);

-- DROP TABLE Offre_Formation CASCADE;
CREATE TABLE Offre_Formation (
    offre_id VARCHAR(7) NOT NULL
    , formation_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , formation_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (formation_id) REFERENCES Formation (formation_id) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE QualiteProfessionnelle CASCADE;
CREATE TABLE QualiteProfessionnelle (
    qualite_professionnelle_id SERIAL NOT NULL PRIMARY KEY
    , qualite_professionnelle_libelle VARCHAR(100)
    , qualite_professionnelle_description VARCHAR(1000)
    , CONSTRAINT qualitepro_unique UNIQUE (qualite_professionnelle_libelle , qualite_professionnelle_description)
);

-- DROP TABLE Offre_QualiteProfessionnelle CASCADE;
CREATE TABLE Offre_QualiteProfessionnelle (
    offre_id VARCHAR(7) NOT NULL
    , qualite_professionnelle_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , qualite_professionnelle_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (qualite_professionnelle_id) REFERENCES QualiteProfessionnelle (qualite_professionnelle_id) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE Qualification CASCADE;
CREATE TABLE Qualification (
    qualification_code INTEGER PRIMARY KEY NOT NULL
    , qualification_libelle VARCHAR(100) NOT NULL
    , CONSTRAINT qualification_unique UNIQUE (qualification_code , qualification_libelle)
);

-- DROP TABLE Offre_Qualification CASCADE;
CREATE TABLE Offre_Qualification (
    offre_id VARCHAR(7) NOT NULL
    , qualification_code INTEGER NOT NULL
    , date_extraction DATE
    -- , PRIMARY KEY (offre_id , qualification_code)
    , PRIMARY KEY (offre_id , qualification_code, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (qualification_code) REFERENCES Qualification (qualification_code) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE Langue CASCADE;
CREATE TABLE Langue (
    langue_id SERIAL NOT NULL PRIMARY KEY
    , langue_libelle VARCHAR(30) NOT NULL
    , langue_code_exigence VARCHAR(1) NOT NULL
    , CONSTRAINT langue_unique UNIQUE (langue_libelle , langue_code_exigence)
);

-- DROP TABLE Offre_Langue CASCADE;
CREATE TABLE Offre_Langue (
    offre_id VARCHAR(7) NOT NULL
    , langue_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , langue_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (langue_id) REFERENCES Langue (langue_id) ON DELETE CASCADE
);

-----------------------------------------------------------------------------------------------------------
-- DROP TABLE PermisConduire CASCADE;
CREATE TABLE PermisConduire (
    permis_id SERIAL NOT NULL PRIMARY KEY
    , permis_libelle VARCHAR(100) NOT NULL
    , permis_code_exigence VARCHAR(1) NOT NULL
    , CONSTRAINT permis_unique UNIQUE (permis_libelle , permis_code_exigence)
);

-- DROP TABLE Offre_PermisConduire CASCADE;
CREATE TABLE Offre_PermisConduire (
    offre_id VARCHAR(7) NOT NULL
    , permis_id INTEGER NOT NULL
    , date_extraction DATE
    , PRIMARY KEY (offre_id , permis_id, date_extraction)
    , FOREIGN KEY (offre_id) REFERENCES OffreEmploi (offre_id) ON DELETE CASCADE
    , FOREIGN KEY (permis_id) REFERENCES PermisConduire (permis_id) ON DELETE CASCADE
);

