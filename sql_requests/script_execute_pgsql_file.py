import os

import psycopg2

current_directory = os.path.dirname(os.path.abspath(__file__))


def read(psql_file):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(current_directory, psql_file), "r") as file:
        return file.read()


query = read(os.path.join("..", "sql_requests", "total_job_offers__city_repartition.pgsql"))


with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        for index, row in enumerate(rows, start=1):
            print(f"{index:03}:  {row}")
