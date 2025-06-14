import json
import os

import psycopg2

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup

conn_id = "my_pg"  # nom du "Connection ID" défini dans la GUI d'Airflow

DB_PARAM = {"database": "francetravail", "host": "postgres_3_0_1", "user": "mhh", "password": "mhh", "port": 5432}  # note : "host" != "localhost"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(CURRENT_DIR, "..", "data", "outputs")

AGGREGATED_JSON_DIR = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file")


@task(task_id="is_only_one_json")
def check_only_one_json_file_in_folder(folder):
    """
    Retourne le chemin du nom du fichier json dans le dossier "folder" s'il n'y a qu'un fichier json dans ce dossier.
    Sinon, s'il y a 0 ou plusieurs fichiers json, on arrête le script.
    """
    json_files = [file for file in os.listdir(folder) if file.endswith(".json")]
    if len(json_files) == 1:
        # return json_files[0]
        return os.path.join(folder, json_files[0])
    else:
        raise Exception(f'Il y a {len(json_files)} fichier(s) json dans le dossier "{folder}": {json_files}')


@task(task_id="load_json")
def load_json(filename):
    """
    Charge simplement le json
    """
    with open(filename, "r") as file:
        offres_data = json.load(file)

    return offres_data


# def fill_db(db_name, attributes_tuple, on_conflict_string):
def fill_db(db_name, attributes_tuple, on_conflict_string, cursor):
    """
    Crée et exécute la requête pour insérer les données dans la table "db_name".

    Évite de devoir construire la requête, et de devoir dupliquer certaines informations comme les attributs.

    Exemple dans le code suivant où on écrit l'attribut date_extraction 4 fois :

        cursor.execute(
            f'''--sql
                INSERT INTO OffreEmploi (offre_id, date_extraction, date_creation, date_actualisation, nombre_postes)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (offre_id) DO UPDATE SET
                    date_extraction = EXCLUDED.date_extraction,
                    date_creation = EXCLUDED.date_creation,
                    date_actualisation = EXCLUDED.date_actualisation,
                    nombre_postes = EXCLUDED.nombre_postes
                ''',
            (offre_id, date_extraction, date_creation, date_actualisation, nombre_postes),
        )

    Avec la fonction, on ne l'écrit plus qu'1 fois :

        fill_db(
            db_name="OffreEmploi",
            attributes_tuple=(
                "offre_id",
                "date_extraction",
                "date_creation",
                "date_actualisation",
                "nombre_postes",
            ),
            on_conflict_string=("offre_id"),
        )

    https://www.postgresql.org/docs/current/sql-insert.html

    Ne retourne rien.
    """

    string_attributs = ", ".join(attributes_tuple)  # pour avoir "attribut1, attribut2, ..." sans les quotes
    placeholders = ", ".join(["%s"] * len(attributes_tuple))  # pour avoir "%s, %s, ..." pour chaque valeur

    query = f"""
        INSERT INTO {db_name} ({string_attributs})
        VALUES ({placeholders})
        ON CONFLICT ({", ".join(on_conflict_string.split(" | "))})
    """

    # Déterminer les colonnes à mettre à jour (toutes sauf celles de la clé)
    update_cols = [f"{attr} = EXCLUDED.{attr}" for attr in attributes_tuple if attr not in on_conflict_string.split(" | ")]

    if update_cols:
        query += f"""DO UPDATE SET {", ".join(update_cols)}"""
    else:
        query += "DO NOTHING"

    cursor.execute(query, tuple(globals().get(attr) for attr in attributes_tuple))
    # conn.commit()  # pas besoin car fait implicitement par la suite avec "with conn.cursor()"

    return None


@task(task_id="table_offre_emploi")
def insert_into_offre_emploi(json_filename):
    """ """

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in json_filename:
                offre_id = offre.get("id")
                date_extraction = offre.get("dateExtraction")
                date_premiere_ecriture = offre.get("datePremiereEcriture")
                date_creation = offre.get("dateCreation").split("T")[0]  # inutile de récupérer l'heure

                date_actualisation_raw = offre.get("dateActualisation")  # rare cas où `"dateActualisation": null` (1 cas sur 50k à l'occurence 7, offre_id 6985803)
                date_actualisation = date_actualisation_raw.split("T")[0] if date_actualisation_raw else None

                nombre_postes = offre.get("nombrePostes")

                # print pour investigation si besoin :
                # print(offre_id, date_extraction, date_premiere_ecriture, date_creation, date_actualisation, nombre_postes, "\n", sep="\n-> ")


                cursor.execute(
                    f"""--sql
                        INSERT INTO OffreEmploi (offre_id, date_extraction, date_premiere_ecriture, date_creation, date_actualisation, nombre_postes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (offre_id) DO UPDATE SET
                            date_extraction = EXCLUDED.date_extraction,
                            date_premiere_ecriture = EXCLUDED.date_premiere_ecriture,
                            date_creation = EXCLUDED.date_creation,
                            date_actualisation = EXCLUDED.date_actualisation,
                            nombre_postes = EXCLUDED.nombre_postes
                        """,
                    (offre_id, date_extraction, date_premiere_ecriture, date_creation, date_actualisation, nombre_postes),
                )

                # fill_db(
                #     db_name="OffreEmploi",
                #     attributes_tuple=(
                #         "offre_id",
                #         "date_extraction",
                #         "date_premiere_ecriture",
                #         "date_creation",
                #         "date_actualisation",
                #         "nombre_postes",
                #     ),
                #     on_conflict_string=("offre_id"),
                # )


with DAG(
    dag_id="DAG_2_WRITE_TO_DB",
    tags=["project"],
) as dag:
    with TaskGroup(group_id="SETUP", tooltip="xxx") as setup:
        create_tables = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="create_all_tables_if_not_existing",
            sql=os.path.join("sql", "create_all_tables.sql"),
        )
        json_file_path = check_only_one_json_file_in_folder(AGGREGATED_JSON_DIR)
        json_content = load_json(json_file_path)

    with TaskGroup(group_id="WRITE_TO_DATABASE", tooltip="xxx") as write:
        with TaskGroup(group_id="INSERT_TO_TABLES", tooltip="xxx") as insert:
            insert_into_offre_emploi(json_content)
