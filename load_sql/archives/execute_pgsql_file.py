import os

import psycopg2

from colorama import Fore, init
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

sql_files_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "1_requests",
    "offers_DE_DA_DS",
)


def read(psql_file):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(sql_files_directory, psql_file), "r") as file:
        return file.read()


sql_files = os.listdir(sql_files_directory)

# si besoin de hardcoder :
sql_files = (
    "01--table_competence.pgsql",
    "02--table_experience.pgsql",
    "03--table_qualiteprofessionnelle.pgsql",
    "04--table_qualification.pgsql",
    "05--table_formation.pgsql",
    "06--table_permisconduire.pgsql",
    "07--table_langue.pgsql",
    "08--table_localisation__1__nom_ville.pgsql",
    "08--table_localisation__2__nom_departement.pgsql",
    "08--table_localisation__3__nom_region.pgsql",
    "09--table_entreprise__1__nom_entreprise__entreprise_adapte.pgsql",
    "09--table_entreprise__2__secteur_activite_libelle.pgsql",
    "10--table_descriptionoffre__1__intitule__description.pgsql",
    "10--table_descriptionoffre__2__nom_partenaire.pgsql",
    "10--table_descriptionoffre__3__rome.pgsql",
    "10--table_descriptionoffre__3__rome_M1811.pgsql",
    "10--table_descriptionoffre__4__difficile_a_pourvoir.pgsql",
    "10--table_descriptionoffre__5__accessible_travailleurs_handicapes.pgsql",
    "11--table_contrat__1__type_contrat.pgsql",
    "11--table_contrat__2__duree_travail.pgsql",
    "11--table_contrat__3__salaire.pgsql",
    "11--table_contrat__4__nature_contrat.pgsql",
    "11--table_contrat__5__alternance.pgsql",
    "11--table_contrat__6__deplacement.pgsql",
    "11--table_contrat__7__condition_specifique.pgsql",
    "12--table_offreemploi__1__dates.pgsql",
    "12--table_offreemploi__2__nombre_postes.pgsql",
)


print(sql_files)

queries = [(file, read(file)) for file in sql_files]


with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
    with conn.cursor() as cursor:
        for filename, query in queries:
            print(f'\n{Fore.CYAN}===> "{filename}"')

            cursor.execute(query)
            rows = cursor.fetchall()

            # Récupérer les noms des colonnes
            headers = ["#"] + [desc[0] for desc in cursor.description]

            # Ajouter les numéros de ligne en première colonne
            rows_with_index = [(index + 1, *row) for index, row in enumerate(rows)]

            # Affichage du tableau avec tabulate
            print(tabulate(rows_with_index, headers=headers, tablefmt="psql"), "\n")
