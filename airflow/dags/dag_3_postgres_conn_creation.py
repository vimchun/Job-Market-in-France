from datetime import datetime, timedelta

import requests

from airflow.models.dag import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

def get_token():
    response = requests.post(
        "http://airflow-apiserver:8080/auth/token",
        json={"username": "airflow", "password": "airflow"},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def create_postgres_conn_v2(**kwargs):
    conn_id = kwargs["conn_id"]

    url = f"http://airflow-apiserver:8080/api/v2/connections/{conn_id}"

    headers = {"Authorization": f"Bearer {get_token()}"}
    response = requests.get(url, headers=headers)

    print("1")
    print(response)
    print("Status:", response.status_code)
    print("Text:", response.text)
    print("Headers:", response.headers)

    if response.status_code == 404:
        payload = {
            "connection_id": conn_id,
            "conn_type": "postgres",
            "host": "postgres",
            "login": "mhh",
            "password": "mhh",
            "port": 5432,
            "schema": "francetravail",
        }
        create_url = "http://airflow-apiserver:8080/api/v2/connections"

        response = requests.post(create_url, json=payload, headers=headers)

        print("2")
        print(response)
        print("Status:", response.status_code)
        print("Text:", response.text)
        print("Headers:", response.headers)

    if response.status_code in [200, 201]:
        print("Connection Created")

    elif response.status_code == 401:
        print("Unauthorized. Invalid token.")

    elif response.status_code == 200:
        print("Connection already exists")

    else:
        print(f"Unexpected status code: {response.status_code}")
        print(response.text)


with DAG(
    dag_id="create_postgres_session",
    default_args={
        "owner": "airflow",
        "start_date": datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=1),
    },
    catchup=False,
) as dag:
    create_conn = PythonOperator(
        task_id="create_postgres_conn_v2",
        python_callable=create_postgres_conn_v2,
        op_kwargs={"conn_id": "postgres_connection"},
    )

    create_conn
