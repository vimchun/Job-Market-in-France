import os

import psycopg2

from colorama import Fore, init
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

sql_files_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "sql_requests",
)


def read(psql_file):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(sql_files_directory, psql_file), "r") as file:
        return file.read()


sql_files = (
    "total_job_offers__region_repartition.pgsql",
    "total_job_offers__department_repartition.pgsql",
    "total_job_offers__city_repartition.pgsql",
)

queries = [(file, read(file)) for file in sql_files]

# with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
#     with conn.cursor() as cursor:
#         for filename, query in queries:
#             print(f'\n{Fore.YELLOW}===== {filename}" =====\n')
#             cursor.execute(query)
#             rows = cursor.fetchall()

#             # Récupérer les noms des colonnes depuis cursor.description
#             headers = [desc[0] for desc in cursor.description]

#             # print(tabulate(rows, headers=headers, tablefmt="fancy_grid"), "\n")  # 'fancy_grid' donne un beau format
#             print(tabulate(rows, headers=headers, tablefmt="psql"), "\n")  # 'fancy_grid' donne un beau format

with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
    with conn.cursor() as cursor:
        for filename, query in queries:
            print(f'\n{Fore.YELLOW}===== "{filename}" =====\n')

            cursor.execute(query)
            rows = cursor.fetchall()

            # for row in rows:
            #     print(*row, type(row))

            # Récupérer les noms des colonnes
            headers = ["#"] + [desc[0] for desc in cursor.description]

            # Ajouter les numéros de ligne en première colonne
            rows_with_index = [(index + 1, *row) for index, row in enumerate(rows)]

            # Affichage du tableau avec tabulate
            print(tabulate(rows_with_index, headers=headers, tablefmt="psql"), "\n")
