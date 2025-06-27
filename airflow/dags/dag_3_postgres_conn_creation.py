from datetime import datetime, timedelta

import requests

from airflow.decorators import task
from airflow.models.dag import DAG

def get_token():
    """
    Récupère le bearer token pour pouvoir faire les requêtes pour GET et POST les connections.
    """
    response = requests.post(
        "http://airflow-apiserver:8080/auth/token",
        json={"username": "airflow", "password": "airflow"},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()

    return response.json()["access_token"]


@task(task_id="check_postgres_connexion")
def check_postgres_connexion(postgres_connection_name):
    """
    Vérifie que la connexion postgres nommée "postgres_connection_name" existe, et la crée le cas échéant (comme si on le faisait depuis la GUI d'Airflow).
    """

    # Requête pour récupérer les informations de la connection nommée "postgres_connection_name"
    response = requests.get(
        url=f"http://airflow-apiserver:8080/api/v2/connections/{postgres_connection_name}",
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    print("** Informations connections existantes **")
    print("   - status_code :", response.status_code)
    print("   - text :", response.text)

    if response.status_code == 200:
        print(f"[OK] La connection {postgres_connection_name} existe déjà.")

    elif response.status_code == 401:
        assert False, "Token invalide (Unauthorized)."

    elif response.status_code == 404:
        print(f"==> La connection {postgres_connection_name} n'existe pas, on va la créer.")
        response_post = requests.post(
            url="http://airflow-apiserver:8080/api/v2/connections",
            json={
                "connection_id": "postgres_connection",
                "conn_type": "postgres",
                "description": "Connection créée avec DAG 2",
                "host": "postgres",
                "login": "mhh",
                "password": "mhh",
                "port": 5432,
                "schema": "francetravail",
            },
            headers={"Authorization": f"Bearer {get_token()}"},
        )

        print(f'** Création de la connection "{postgres_connection_name}" **')
        print("   - status_code :", response_post.status_code)
        print("   - text :", response_post.text)

        assert response_post.status_code == 201, "On doit avoir status_code = 201"  # 201 si la connection est bien crée

    else:
        print(f"Status code: {response.status_code}")
        print(f"Response text : {response.text}")

        assert False, f"Erreur sur la création de la connection {postgres_connection_name}"


with DAG(
    dag_id="create_postgres_session",
    # default_args={
    #     "owner": "airflow",
    #     "start_date": datetime.now().replace(second=0, microsecond=0) - timedelta(minutes=1),
    # },
    # catchup=False,
) as dag:
    check_postgres_connexion("postgres_connection")
