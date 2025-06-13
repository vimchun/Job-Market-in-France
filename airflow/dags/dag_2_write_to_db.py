from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

conn_id = "my_pg"  # nom du "Connection ID" défini dans la GUI d'Airflow

with DAG(
    dag_id="dag_2_write_to_db",
    tags=["project"],
) as dag:
    create_tables = SQLExecuteQueryOperator(
        conn_id=conn_id,
        task_id="create_table",
        sql="sql/create_all_tables.sql",
    )
