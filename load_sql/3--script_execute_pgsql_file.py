import json
import os
import sys

import psycopg2

# proposition de dbt ?

current_directory = os.path.dirname(os.path.abspath(__file__))


def read(psql_file):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(current_directory, psql_file), "r") as file:
        return file.read()


query = read(os.path.join("requests", "check_creation_table.pgsql"))

# print(query)
conn = psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)


cursor = conn.cursor()


cursor.execute(query)
rows = cursor.fetchall()

for index, row in enumerate(rows, start=1):
    print(f"{index:03}:  {row}")

cursor.close()
conn.close()
