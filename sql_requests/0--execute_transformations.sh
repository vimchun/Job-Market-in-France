# Script pour lancer les scripts SQL pour les transformations :
#  - Ajouts des attributs :
#    - `metier_data`
#    - `salaire_min`
#    - `salaire_max`
#    - `liste_mots_cles`
#
#  - Mise à jour :
#    - des valeurs `DE`, `DA` ou `DS` pour la colonne `metier_data`
#    - de la liste des mots-clés pour la colonne `liste_mots_cles`
#

# Pour lancer ce script : `bash sql_requests/0--execute_transformations.sh`

docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/0--add_columns.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/1--update__table_descriptionoffre__column__metier_data__DE.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/2--update__table_descriptionoffre__column__metier_data__DA.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/3--update__table_descriptionoffre__column__metier_data__DS.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/4--update__table_contrat__columns__salaire_min__salaire_max.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/5--update__table_descriptionoffre__column__liste_mots_cles.pgsql
