import json

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
    token = get_token()

    for _ in range(2):
        """
        Boucle pour itérer 2 fois uniquement (pour éviter un while), pour :
        1. GET connection
        2. Si existe avec bons params => break
        3. Sinon DELETE connection + création connection => continue
        4. Si création OK => break
        """

        # Requête pour récupérer les informations de la connection nommée "postgres_connection_name"
        response = requests.get(
            url=f"http://airflow-apiserver:8080/api/v2/connections/{postgres_connection_name}",
            headers={"Authorization": f"Bearer {token}"},
        )

        print("** Informations connections existantes **")
        print("   - status_code :", response.status_code)
        print("   - text :", response.text)  # string

        conn_dict_to_create = {
            "connection_id": postgres_connection_name,
            "conn_type": "postgres",
            "description": "Connection créée avec DAG 2",
            "host": "postgres",
            "login": "mhh",
            "password": "mhh",
            "port": 5432,
            "schema": "francetravail",
            "extra": None,
        }

        if response.status_code == 200:
            current_connection_json = json.loads(response.text)  # on passe le string en dict

            # On compare certains champs des 2 jsons pour s'assurer que la connection "postgres_connection_name" a les bons paramètres
            fields_to_compare = ["conn_type", "description", "host", "login", "port", "schema"]

            subset_current = {k: current_connection_json[k] for k in fields_to_compare}
            subset_to_create = {k: conn_dict_to_create[k] for k in fields_to_compare}

            if subset_current != subset_to_create:
                print(f'La connection "{postgres_connection_name}" existe déjà mais les paramètres ne sont pas comme ceux désirés.')

                response_delete = requests.delete(
                    url=f"http://airflow-apiserver:8080/api/v2/connections/{postgres_connection_name}",
                    headers={"Authorization": f"Bearer {token}"},
                )

                print("** Suppression de la connection (car paramètres différents de ceux désirés) **")
                print("   - status_code :", response_delete.status_code)
                print("   - text :", response_delete.text)

                continue  # on passe à l'occurence suivante de la boucle for

            print(f'La connection "{postgres_connection_name}" existe déjà avec les bons paramètres.')

            break  # on sort de la boucle for, si pas de problème au niveau comparaison des params

        elif response.status_code == 401:
            raise ValueError("Token invalide (Unauthorized).")

        elif response.status_code == 404:
            print(f'==> La connection "{postgres_connection_name}" n\'existe pas, on va la créer.')
            response_post = requests.post(
                url="http://airflow-apiserver:8080/api/v2/connections",
                json=conn_dict_to_create,
                headers={"Authorization": f"Bearer {token}"},
            )

            print(f'** Création de la connection "{postgres_connection_name}" **')
            print("   - status_code :", response_post.status_code)
            print("   - text :", response_post.text)

            if response_post.status_code != 201:  # 201 si la connection est bien crée
                raise ValueError(f'La connection "{postgres_connection_name}" n\'est pas bien créée.')

            break  # on sort de la boucle for

        else:
            print(f"Status code: {response.status_code}")
            print(f"Response text : {response.text}")

            raise ValueError(f'Problème avec la connection "{postgres_connection_name}"')


with DAG(dag_id="create_postgres_session") as dag:
    check_postgres_connexion("postgres_connection")
