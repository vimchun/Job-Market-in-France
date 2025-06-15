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


def create_and_execute_insert_query(table_name: str, row_data: dict, conflict_columns: list, cursor):
    """
    https://www.postgresql.org/docs/current/sql-insert.html

    Insère ou met à jour une ligne dans une table PostgreSQL.

    Paramètres :
      - table_name (str) : nom de la table
      - row_data (dict) : données à insérer (clé = colonne, valeur = donnée)
      - conflict_columns (list) : liste des colonnes utilisées pour "ON CONFLICT"
      - cursor : cursor psycopg2


    Exemple :

        offre_id = "188VMCV"
        date_extraction = "2025-06-15"
        nombre_postes = 3

        fill_db(
            db_table="OffreEmploi",
            row_data={
                "offre_id": offre_id,
                "date_extraction": date_extraction,
                "nombre_postes": nombre_postes,
            },
            conflict_columns=["offre_id"],
            cursor,
        )

                <==>

        cursor.execute(
            f'''--sql
                INSERT INTO OffreEmploi (offre_id, date_extraction, nombre_postes)
                VALUES (%s, %s, %s)
                ON CONFLICT (offre_id) DO UPDATE SET
                    date_extraction = EXCLUDED.date_extraction,
                    nombre_postes = EXCLUDED.nombre_postes
                ''',
            (offre_id, date_extraction, nombre_postes),
        )


    Ne retourne rien
    """

    columns = list(row_data.keys())
    values = list(row_data.values())

    columns_str = ", ".join(columns)  # pour avoir "attribut1, attribut2, ..." sans les quotes
    placeholders = ", ".join(["%s"] * len(columns))  # pour avoir "%s, %s, ..." (1* "%s" par colonne)

    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT ({", ".join(conflict_columns)})
    """

    update_columns = [f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_columns]
    if update_columns:
        query += f" DO UPDATE SET {', '.join(update_columns)}"
    else:
        query += " DO NOTHING"

    cursor.execute(query, values)


@task(task_id="table_offre_emploi")
def insert_into_offre_emploi(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table OffreEmploi"""

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

                create_and_execute_insert_query(
                    table_name="OffreEmploi",
                    row_data={
                        "offre_id": offre_id,
                        "date_extraction": date_extraction,
                        "date_premiere_ecriture": date_premiere_ecriture,
                        "date_creation": date_creation,
                        "date_actualisation": date_actualisation,
                        "nombre_postes": nombre_postes,
                    },
                    conflict_columns=["offre_id"],
                    cursor=cursor,
                )


@task(task_id="table_contrat")
def insert_into_contrat(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Contrat"""

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in json_filename:
                offre_id = offre.get("id")

                type_contrat = offre.get("typeContrat")
                type_contrat_libelle = offre.get("typeContratLibelle")
                duree_travail_libelle = offre.get("dureeTravailLibelle")
                duree_travail_libelle_converti = offre.get("dureeTravailLibelleConverti")
                nature_contrat = offre.get("natureContrat")
                salaire_libelle = offre.get("salaire").get("libelle")
                salaire_complement_1 = offre.get("salaire").get("complement1")
                salaire_complement_2 = offre.get("salaire").get("complement2")
                salaire_commentaire = offre.get("salaire").get("commentaire")
                alternance = offre.get("alternance")
                deplacement_code = offre.get("deplacementCode")
                deplacement_libelle = offre.get("deplacementLibelle")
                temps_travail = offre.get("complementExercice")
                condition_specifique = offre.get("conditionExercice")

                # print pour investigation si besoin :
                # print(
                #     offre_id, type_contrat, type_contrat_libelle, duree_travail_libelle, duree_travail_libelle_converti, nature_contrat, salaire_libelle,
                #     salaire_complement_1, salaire_complement_2, salaire_commentaire, alternance, deplacement_code, deplacement_libelle, temps_travail, condition_specifique, sep="\n-> ",
                # )  # fmt:off

                create_and_execute_insert_query(
                    table_name="Contrat",
                    row_data={
                        "offre_id": offre_id,
                        "type_contrat": type_contrat,
                        "type_contrat_libelle": type_contrat_libelle,
                        "duree_travail_libelle": duree_travail_libelle,
                        "duree_travail_libelle_converti": duree_travail_libelle_converti,
                        "nature_contrat": nature_contrat,
                        "salaire_libelle": salaire_libelle,
                        "salaire_complement_1": salaire_complement_1,
                        "salaire_complement_2": salaire_complement_2,
                        "salaire_commentaire": salaire_commentaire,
                        "alternance": alternance,
                        "deplacement_code": deplacement_code,
                        "deplacement_libelle": deplacement_libelle,
                        "temps_travail": temps_travail,
                        "condition_specifique": condition_specifique,
                    },
                    conflict_columns=["offre_id"],
                    cursor=cursor,
                )


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
            insert_into_contrat(json_content)
