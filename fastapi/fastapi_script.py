# cd fastapi/
# uvicorn fastapi_script:app --reload
# uvicorn fastapi_script:app --reload  --log-level debug

import os

from datetime import datetime
from textwrap import dedent  # used to dedent variable strings that are indented because defined on a function
from typing import Optional

import pandas as pd
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

location_csv_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "api_extract__transform",
    "locations_information",
    "code_name__city_department_region.csv",
)

df_location = pd.read_csv(
    location_csv_file,
    usecols=["code_region", "nom_region", "code_departement", "nom_departement", "code_postal", "nom_ville"],
    dtype={"code_region": str, "nom_region": str, "code_departement": str, "nom_departement": str, "code_postal": str, "nom_ville": str},
)


# Fonction pour centraliser les filtres
def set_endpoints_filters(
    metier_data: Optional[str] = Query(default=None, description='Valeurs possibles : "DE", "DA", "DS" _(champ vide = pas de filtre)_'),
    date_creation_min: Optional[str] = Query(
        default=None, description='Filtrer par date de création, par exemple les offres à partir de "2025-04-25" (format "YYYY-MM-DD") _(champ vide = pas de filtre)_'
    ),
    code_region: Optional[str] = Query(
        default=None,
        description=dedent("""\
            Filtrer sur le code de la région (champ vide = pas de filtre).\n
            <i> Valeurs possibles :
            [11] Île-de-France, [24] Centre-Val de Loire, [27] Bourgogne-Franche-Comté, [28] Normandie,
            [32] Hauts-de-France, [44] Grand Est, [52] Pays de la Loire, [53] Bretagne, [75] Nouvelle-Aquitaine,
            [76] Occitanie, [84] Auvergne-Rhône-Alpes, [93] Provence-Alpes-Côte d'Azur </i> """),
    ),
    nom_region: Optional[str] = Query(default=None, description="Filtrer sur le nom de la région _(champ vide = pas de filtre)_"),
    code_departement: Optional[str] = Query(default=None, description="Filtrer sur le code du département _(champ vide = pas de filtre)_"),
    nom_departement: Optional[str] = Query(default=None, description="Filtrer sur le nom du département _(champ vide = pas de filtre)_"),
    code_postal: Optional[str] = Query(default=None, description="Filtrer sur le code de la ville _(champ vide = pas de filtre)_"),
    nom_ville: Optional[str] = Query(default=None, description="Filtrer sur le nom de la ville _(champ vide = pas de filtre)_"),
):
    # Validation de `metier_data`
    allowed_metier_data = {"DE", "DA", "DS", None}  # set

    if metier_data not in allowed_metier_data:
        raise HTTPException(status_code=400, detail=f"'metier_data' doit être vide ou valoir 'DE', 'DA' ou 'DS'")

    # Validation de `date_creation_min`
    if date_creation_min:
        try:
            datetime.strptime(date_creation_min, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Format invalide pour 'date_creation_min' (attendu : YYYY-MM-DD)")

    # Validation de `code_region`
    if code_region is not None and code_region not in df_location["code_region"].values:
        raise HTTPException(status_code=400, detail=f"Le code région '{code_region}' est invalide.")

    # Validation de `nom_region`
    if nom_region is not None and nom_region not in df_location["nom_region"].values:
        raise HTTPException(status_code=400, detail=f"Le nom de la région '{nom_region}' est invalide.")

    # Validation de `code_departement`
    if code_departement is not None and code_departement not in df_location["code_departement"].values:
        raise HTTPException(status_code=400, detail=f"Le code département '{code_departement}' est invalide.")

    # Validation de `nom_departement`
    if nom_departement is not None and nom_departement not in df_location["nom_departement"].values:
        raise HTTPException(status_code=400, detail=f"Le nom du département '{nom_departement}' est invalide.")

    # Validation de `code_postal`
    if code_postal is not None and code_postal not in df_location["code_postal"].values:
        raise HTTPException(status_code=400, detail=f"Le code postal '{code_postal}' est invalide.")

    # Validation de `nom_ville`
    if nom_ville is not None and nom_ville not in df_location["nom_ville"].values:
        raise HTTPException(status_code=400, detail=f"Le nom de la ville '{nom_ville}' est invalide.")

    return {
        "metier_data": metier_data,
        "date_creation_min": date_creation_min,
        "code_region": code_region,
        "nom_region": nom_region,
        "code_departement": code_departement,
        "nom_departement": nom_departement,
        "code_postal": code_postal,
        "nom_ville": nom_ville,
    }


# Fonction de filtrage qui modifie la requête SQL selon les paramètres
def execute_modified_sql_request_with_filters(
    sql_files_directory_part_2,
    metier_data,
    date_creation_min,
    code_region,
    nom_region,
    code_departement,
    nom_departement,
    code_postal,
    nom_ville,
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

        # Filtrage par "code_region"
        if code_region is None:
            sql_file_content = sql_file_content.replace("AND code_region = 'placeholder_code_region'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_code_region'", "%s")
            params.append(code_region)

        # Filtrage par "nom_region"
        if nom_region is None:
            sql_file_content = sql_file_content.replace("AND nom_region = 'placeholder_nom_region'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_nom_region'", "%s")
            params.append(nom_region)

        # Filtrage par "code_departement"
        if code_departement is None:
            sql_file_content = sql_file_content.replace("AND code_departement = 'placeholder_code_departement'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_code_departement'", "%s")
            params.append(code_departement)

        # Filtrage par "nom_departement"
        if nom_departement is None:
            sql_file_content = sql_file_content.replace("AND nom_departement = 'placeholder_nom_departement'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_nom_departement'", "%s")
            params.append(nom_departement)

        # Filtrage par "code_postal"
        if code_postal is None:
            sql_file_content = sql_file_content.replace("AND code_postal = 'placeholder_code_postal'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_code_postal'", "%s")
            params.append(code_postal)

        # Filtrage par "nom_ville"
        if nom_ville is None:
            sql_file_content = sql_file_content.replace("AND nom_ville = 'placeholder_nom_ville'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_nom_ville'", "%s")
            params.append(nom_ville)

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

    sql_file_directory_part_2 = os.path.join("01_table_Competence", "competences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")

    # tronquer la colonne "libelle" à 60 caractères pour chaque ligne, sinon le tableau s'affichera mal sur Open API
    truncated_result = [(row[0], row[1], row[2][:60] if row[2] else row[2], row[3]) for row in result]

    table = tabulate(truncated_result, headers=["nb occurences", "code", "libelle", "code exigence"], tablefmt="psql").replace("'", " ")
    # note : on remplace les guillemets simples parce que ce qui se trouve entre 2 guillemets simples est écrit en vert sur Open API

    return Response(content=table, media_type="text/plain")


@app.get("/description_offre/total_offres", tags=['Table "Description_Offre"'])
def get_number_of_offers(filters: dict = Depends(set_endpoints_filters)):
    """Nombre total d'offres d'emploi."""

    sql_file_directory_part_2 = os.path.join("10_table_DescriptionOffre", "0__total_offres.pgsql")

    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="one")

    total_offres = result[0] if result else 0

    return Response(content=f"total offres = {total_offres}", media_type="text/plain")
