# cd fastapi/
# uvicorn fastapi_script:app --reload
# uvicorn fastapi_script:app --reload  --log-level debug


import os

from datetime import datetime
from typing import Optional

import psycopg2

from colorama import Fore, init
from pydantic import BaseModel, field_validator
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

from fastapi import Depends, FastAPI, HTTPException, Query, Response  # status

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


app = FastAPI(
    title="API sur les offres d'emploi chez France Travail",
    description="description à remplir",
    openapi_tags=[
        {"name": 'Table "Offre_Emploi"'},
        {"name": 'Table "Competence"'},
        {"name": 'Table "Experience"'},
        {"name": 'Table "Qualite_Professionnelle"'},
        {"name": 'Table "Qualification"'},
        {"name": 'Table "Formation"'},
        {"name": 'Table "Permis_Conduire"'},
        {"name": 'Table "Langue"'},
        {"name": 'Table "Localisation"'},
        {"name": 'Table "Entreprise"'},
        {"name": 'Table "Description_Offre"'},
        {"name": 'Table "Contrat"'},
    ],
)

sql_file_directory_part_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql_requests")


# Fonction pour centraliser les filtres
def set_endpoints_filters(
    metier_data: Optional[str] = Query(
        default=None,
        description='Valeurs possibles : "DE", "DA", "DS" _(champ vide pour ne pas filtrer)_',
    ),
    date_creation_min: Optional[str] = Query(
        default=None,
        description='Filtrer par date de création, par exemple les offres à partir de "2025-04-25" (format "YYYY-MM-DD") _(champ vide pour ne pas filtrer)_',
    ),
):
    # Validation de `metier_data`
    allowed_metier_data = {"DE", "DA", "DS", None}  # set

    if metier_data not in allowed_metier_data:
        raise HTTPException(
            status_code=400,
            detail=f"'metier_data' doit être vide ou valoir 'DE', 'DA' ou 'DS'",
        )

    # Validation de `date_creation_min`
    if date_creation_min:
        try:
            datetime.strptime(date_creation_min, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Format invalide pour 'date_creation_min' (attendu : YYYY-MM-DD)",
            )

    return {
        "metier_data": metier_data,
        "date_creation_min": date_creation_min,
    }


# Fonction de filtrage qui modifie la requête SQL selon les paramètres
def execute_modified_sql_request_with_filters(
    sql_files_directory_part_2,
    metier_data,
    date_creation_min,
    fetch="all",
):
    """
    Prend en entrée le fichier sql dont le chemin se termine par la paramètre "sql_files_directory_part_2"
      et applique les filtres sur la requête SQL en fonction des paramètres fournis.

    Retourne le contenu du fichier sql modifié, et les paramètres.
    """
    params = []

    with open(os.path.join(sql_file_directory_part_1, sql_files_directory_part_2), "r") as file:
        sql_file_content = file.read()

        print(f'\n{Fore.CYAN}===> requête depuis le fichier "{sql_files_directory_part_2}"')

        # Filtrage par "metier_data"
        if metier_data is None:
            sql_file_content = sql_file_content.replace("metier_data = 'placeholder_metier_data'", "1=1")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_metier_data'", "%s")
            params.append(metier_data)

        # Filtrage par "date_creation_min"
        if date_creation_min is None:
            sql_file_content = sql_file_content.replace("AND date_creation >= 'placeholder_date_creation_min'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_date_creation_min'", "%s")
            params.append(date_creation_min)

        modified_sql_file_content = sql_file_content

        with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
            with conn.cursor() as cursor:
                cursor.execute(modified_sql_file_content, tuple(params))
                if fetch == "all":
                    return cursor.fetchall()
                elif fetch == "one":
                    return cursor.fetchone()


@app.get("/competence", tags=['Table "Competence"'])
def get_competences(filters: dict = Depends(set_endpoints_filters)):
    """Compétences triées par code exigence ((E)xigé d'abord, puis (S)ouhaité), par nombre d'occurences (DESC) et par code (ASC)."""
    metier_data = filters["metier_data"]
    date_creation_min = filters["date_creation_min"]

    sql_file_directory_part_2 = os.path.join("01_table_Competence", "competences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, metier_data, date_creation_min, fetch="all")

    # tronquer la colonne "libelle" à 60 caractères pour chaque ligne, sinon le tableau s'affichera mal sur Open API
    truncated_result = [(row[0], row[1], row[2][:60] if row[2] else row[2], row[3]) for row in result]

    table = tabulate(truncated_result, headers=["nb occurences", "code", "libelle", "code exigence"], tablefmt="psql").replace("'", " ")
    # note : on remplace les guillemets simples parce que ce qui se trouve entre 2 guillemets simples est écrit en vert sur Open API

    return Response(content=table, media_type="text/plain")


@app.get("/description_offre/total_offres", tags=['Table "Description_Offre"'])
def get_number_of_offers(filters: dict = Depends(set_endpoints_filters)):
    """Nombre total d'offres d'emploi."""
    metier_data = filters["metier_data"]
    date_creation_min = filters["date_creation_min"]

    sql_file_directory_part_2 = os.path.join("10_table_DescriptionOffre", "0__total_offres.pgsql")

    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, metier_data, date_creation_min, fetch="one")

    total_offres = result[0] if result else 0

    return Response(content=f"total offres = {total_offres}", media_type="text/plain")
