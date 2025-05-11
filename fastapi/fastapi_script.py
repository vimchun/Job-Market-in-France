# cd fastapi/
# uvicorn fastapi_script:app --reload
# uvicorn fastapi_script:app --reload  --log-level debug


import os

from typing import Optional

import psycopg2

from colorama import Fore, init
from pydantic import BaseModel, field_validator
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

from fastapi import FastAPI, HTTPException, Query  # status

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


app = FastAPI()

sql_files_directory_part_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql_requests")


def get_conn():
    return psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)


def read_sql_file(sql_files_directory_part_2):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(sql_files_directory_part_1, sql_files_directory_part_2), "r") as file:
        return file.read()


@app.get("/")
def get_number_of_offers(
    metier_data: Optional[str] = Query(default=None),
    date_min: Optional[str] = Query(default=None),  # format 'YYYY-MM-DD'
):
    allowed_metier_data = {"DE", "DA", "DS", None}  # set

    if metier_data not in allowed_metier_data:
        raise HTTPException(
            status_code=400,
            detail=f"'metier_data' doit être vide ou valoir 'DE', 'DA' ou 'DS'",
        )

    with get_conn() as conn:
        with conn.cursor() as cursor:
            sql_files_directory_part_2 = os.path.join("10_table_DescriptionOffre", "0__total_offres.pgsql")
            sql_file_content = read_sql_file(sql_files_directory_part_2)

            print(f'\n{Fore.CYAN}===> requête depuis le fichier "{sql_files_directory_part_2}"')

            params = []

            # metier_data
            if metier_data is None:
                sql_file_content = sql_file_content.replace("metier_data = 'placeholder_metier_data'", "1=1")
            else:
                sql_file_content = sql_file_content.replace("'placeholder_metier_data'", "%s")
                params.append(metier_data)

            # date_min
            if date_min is None:
                sql_file_content = sql_file_content.replace("AND date_creation >= 'placeholder_date_min'", "")
            else:
                sql_file_content = sql_file_content.replace("'placeholder_date_min'", "%s")
                params.append(date_min)

            # exécution
            cursor.execute(sql_file_content, tuple(params))
            result = cursor.fetchone()
            total_offres = result[0] if result else 0

            return {"total_offres": total_offres}


################################################################################################################################################################
if 0:
    """Pour exécuter une requête sql avec les placeholders et afficher les résultats dans la console (en dehors de FastAPI donc)"""

    def execute_request_without_fastapi(metier_data=None, date_min=None):
        """Pour voir le résultat de la requête dans la console"""
        with get_conn() as conn:
            with conn.cursor() as cursor:
                sql_files_directory_part_2 = os.path.join("10_table_DescriptionOffre", "0__total_offres.pgsql")
                sql_file_content = read_sql_file(sql_files_directory_part_2)

                print(f'\n{Fore.CYAN}===> requête depuis le fichier "{sql_files_directory_part_2}"')

                params = []

                # metier_data
                if metier_data is None:
                    sql_file_content = sql_file_content.replace("metier_data = 'placeholder_metier_data'", "1=1")
                else:
                    sql_file_content = sql_file_content.replace("'placeholder_metier_data'", "%s")
                    params.append(metier_data)

                # date_min
                if date_min is None:
                    sql_file_content = sql_file_content.replace("AND date_creation >= 'placeholder_date_min'", "")
                else:
                    sql_file_content = sql_file_content.replace("'placeholder_date_min'", "%s")
                    params.append(date_min)

                # exécution
                cursor.execute(sql_file_content, tuple(params))

                rows = cursor.fetchall()

                headers = ["#"] + [desc[0] for desc in cursor.description]  # Récupérer les noms des colonnes
                rows_with_index = [(index + 1, *row) for index, row in enumerate(rows)]  # Ajouter les numéros de ligne en première colonne
                print(tabulate(rows_with_index, headers=headers, tablefmt="psql"), "\n")  # Affichage du tableau avec tabulate

    execute_request_without_fastapi(
        metier_data="DE",  # metier_data = None, "DE", "DA" ou "DS"
        date_min=None,
    )
