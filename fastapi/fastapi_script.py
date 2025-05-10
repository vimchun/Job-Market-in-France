# cd fastapi/
# uvicorn fastapi_script:app --reload

import os

from typing import Optional

import psycopg2

from colorama import Fore, init
from pydantic import BaseModel, field_validator
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

from fastapi import FastAPI, HTTPException, Query  # status

# from fastapi.security import HTTPBasic, HTTPBasicCredentials

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


sql_files_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "sql_requests",
    "1_requests",
    "offers_DE_DA_DS",
)


def read(psql_file):
    """Simple fonction pour gagner une ligne de code pour que le code soit plus simple à écrire/lire"""
    with open(os.path.join(sql_files_directory, psql_file), "r") as file:
        return file.read()


sql_files = os.listdir(sql_files_directory)


# si besoin de hardcoder :
sql_files = [
    # "00--table_offreemploi__1__dates.pgsql",
    # "00--table_offreemploi__2__nombre_postes.pgsql",
    # "01--table_competence.pgsql",
    # "02--table_experience.pgsql",
    # "03--table_qualiteprofessionnelle.pgsql",
    # "04--table_qualification.pgsql",
    # "05--table_formation.pgsql",
    # "06--table_permisconduire.pgsql",
    # "07--table_langue.pgsql",
    # "08--table_localisation__1__nom_ville.pgsql",
    # "08--table_localisation__2__nom_departement.pgsql",
    # "08--table_localisation__3__nom_region.pgsql",
    # "09--table_entreprise__1__nom_entreprise__entreprise_adapte.pgsql",
    # "09--table_entreprise__2__secteur_activite_libelle.pgsql",
    "10--table_descriptionoffre__0__total_offres.pgsql",
    # "10--table_descriptionoffre__1__intitule__description.pgsql",
    # "10--table_descriptionoffre__1__liste_mots_cles.pgsql",
    # "10--table_descriptionoffre__1__TRANSFORMATION__description__add_keywords_list.pgsql",
    # "10--table_descriptionoffre__2__nom_partenaire.pgsql",
    # "10--table_descriptionoffre__3__rome.pgsql",
    # "10--table_descriptionoffre__3__rome_M1811.pgsql",
    # "10--table_descriptionoffre__4__difficile_a_pourvoir.pgsql",
    # "10--table_descriptionoffre__5__accessible_travailleurs_handicapes.pgsql",
    # "11--table_contrat__1__type_contrat.pgsql",
    # "11--table_contrat__2__duree_travail.pgsql",
    # "11--table_contrat__3__nature_contrat.pgsql",
    # "11--table_contrat__4__salaire.pgsql",
    # "11--table_contrat__4__TRANSFORMATION__add_salaire.pgsql",
    # "11--table_contrat__5__alternance.pgsql",
    # "11--table_contrat__6__deplacement.pgsql",
    # "11--table_contrat__7__condition_specifique.pgsql",
]

print(sql_files)


queries = [(file, read(file)) for file in sql_files]
# sql_files = [f for f in os.listdir(sql_files_directory) if f.endswith(".pgsql")]  # mieux ?

app = FastAPI()


def get_conn():
    return psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)


@app.get("/")
def get_number_of_offers(metier_data: Optional[str] = Query(default=None)):
    allowed_metier_data = {"DE", "DA", "DS"}

    if metier_data and metier_data not in allowed_metier_data:
        raise HTTPException(
            status_code=400,
            detail=f"'metier_data' doit être vide ou valoir 'DE', 'DA' ou 'DS'",
        )

    with get_conn() as conn:
        with conn.cursor() as cursor:
            for filename, query in queries:
                print(f'\n{Fore.CYAN}===> requête depuis le fichier "{filename}"')

                if metier_data is None:  # si pas de filtre, on remplace toute la ligne par "1=1"
                    sql = query.replace("metier_data = 'placeholder_metier_data'", "1=1")
                    cursor.execute(sql)
                else:  # on injecte la valeur
                    sql = query.replace("'placeholder_metier_data'", "%s")
                    cursor.execute(sql, (metier_data,))

                result = cursor.fetchone()
                total_offres = result[0] if result else 0

                return {"total_offres": total_offres}


def execute_request_without_fastapi(metier_data=None):
    """
    To see the request result on the console
    """
    with get_conn() as conn:
        with conn.cursor() as cursor:
            for filename, query in queries:
                print(f'\n{Fore.CYAN}===> "{filename}"')

                if metier_data is None:  # si pas de filtre, on remplace toute la ligne par "1=1"
                    sql = query.replace("metier_data = 'placeholder_metier_data'", "1=1")
                    cursor.execute(sql)
                else:  # on injecte la valeur
                    sql = query.replace("'placeholder_metier_data'", "%s")
                    cursor.execute(sql, (metier_data,))

                rows = cursor.fetchall()

                headers = ["#"] + [desc[0] for desc in cursor.description]  # Récupérer les noms des colonnes
                rows_with_index = [(index + 1, *row) for index, row in enumerate(rows)]  # Ajouter les numéros de ligne en première colonne
                print(tabulate(rows_with_index, headers=headers, tablefmt="psql"), "\n")  # Affichage du tableau avec tabulate


# execute_request_without_fastapi(metier_data=None)  # metier_data = None, "DE", "DA" ou "DS"
