# script to launch SQL scripts for transformations :
#  - add the attribute `metier_data`
#  - update the value to `DE`, `DA` or `DS`

# to launch this script : `bash sql_requests/0--execute_transformations.sh`

docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/0--add_columns__metier_data.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/1--update__metier_data__DE.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/2--update__metier_data__DA.pgsql
docker exec -i pg_container_job_market psql -U mhh -d francetravail <sql_requests/0_transformations/3--update__metier_data__DS.pgsql
