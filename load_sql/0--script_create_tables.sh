# script to create all tables
docker exec -i pg_container_job_market psql -U mhh -d francetravail <load_sql/sql_files/tables_deletion_creation/creation.sql
