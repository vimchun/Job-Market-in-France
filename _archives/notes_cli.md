Quelques commandes en vrac qui peuvent servir :

```bash

# [bash] investiguer pb de connexion
docker logs pg_container_job_market -f

# [bash] se connecter au conteneur postgresql
docker exec -it pg_container_job_market bash

# [docker] supprimer la base francetravail
dropdb -h localhost -U mhh francetravail

# [docker] créer la base francetravail
createdb -h localhost -U mhh francetravail

# [docker] se connecter à la base francetravail
psql -h localhost -U mhh -d francetravail -p 5432  # en précisant le port
psql -h localhost -U mhh -d francetravail


# docker exec -i pg_container_job_market psql -U mhh -c "CREATE DATABASE jobtest;"


# se connecter au conteneur postgres pour vérifier les tables
docker exec -it postgres_container bash
psql -U mhh -d francetravail


docker compose up airflow-init

```



```sql
-- supprimer contenu d'une table, sans supprimer la table
TRUNCATE TABLE [nom_de_la_table];

-- Supprimer toutes les entrées d'une table
DELETE FROM [nom_de_la_table]

-- \d table
francetravail=# \d competence
                                                  Table "public.competence"
          Column          |          Type          | Collation | Nullable |                      Default
--------------------------+------------------------+-----------+----------+---------------------------------------------------
 competence_id            | integer                |           | not null | nextval('competence_competence_id_seq'::regclass)
 competence_code          | character varying(6)   |           |          |
 competence_libelle       | character varying(500) |           |          |
 competence_code_exigence | character varying(1)   |           |          |
Indexes:
    "competence_pkey" PRIMARY KEY, btree (competence_id)
    "competence_unique" UNIQUE CONSTRAINT, btree (competence_code, competence_libelle, competence_code_exigence)


-- \di
francetravail=# \di
                                     List of relations
 Schema |               Name                | Type  | Owner |            Table
--------+-----------------------------------+-------+-------+------------------------------
 public | competence_pkey                   | index | mhh   | competence
 public | competence_unique                 | index | mhh   | competence
 public | contrat_pkey                      | index | mhh   | contrat
 public | descriptionoffre_pkey             | index | mhh   | descriptionoffre
 public | domaineformation_pkey             | index | mhh   | domaineformation
 public | entreprise_pkey                   | index | mhh   | entreprise
 public | experience_pkey                   | index | mhh   | experience
 public | langue_pkey                       | index | mhh   | langue
 public | localisation_pkey                 | index | mhh   | localisation
 public | niveauformation_pkey              | index | mhh   | niveauformation
 public | offre_competence_pkey             | index | mhh   | offre_competence
 public | offre_domaineformation_pkey       | index | mhh   | offre_domaineformation
 public | offre_experience_pkey             | index | mhh   | offre_experience
 public | offre_langue_pkey                 | index | mhh   | offre_langue
 public | offre_niveauformation_pkey        | index | mhh   | offre_niveauformation
 public | offre_permisconduire_pkey         | index | mhh   | offre_permisconduire
 public | offre_qualification_pkey          | index | mhh   | offre_qualification
 public | offre_qualiteprofessionnelle_pkey | index | mhh   | offre_qualiteprofessionnelle
 public | offreemploi_pkey                  | index | mhh   | offreemploi
 public | permisconduire_pkey               | index | mhh   | permisconduire
 public | qualification_pkey                | index | mhh   | qualification
 public | qualiteprofessionnelle_pkey       | index | mhh   | qualiteprofessionnelle
 public | unique_experience                 | index | mhh   | experience
(23 rows)

```