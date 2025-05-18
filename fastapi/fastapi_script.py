# cd fastapi/  &&  uvicorn fastapi_script:app --reload
# cd fastapi/  &&  uvicorn fastapi_script:app --reload  --log-level debug

"""
todo :
supprimer les param noms : région département ville
créer des routes pour avoir le mapping nom - code
"""

import os

from datetime import datetime
from textwrap import dedent  # pour gérer les indentations
from typing import List, Optional

import pandas as pd
import psycopg2

from colorama import Fore, Style, init
from pydantic import BaseModel, field_validator
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

from fastapi import Depends, FastAPI, HTTPException, Query, Response  # status

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


tag_all_offres = "Pour toutes les offres d'emploi"
tag_location_mapping_name_code = "Mapping nom <> code région, département, ville"

message_on_endpoints_about_fields = "<u>Paramètres :</u> chaque champ est facultatif (champ vide = pas de filtre)."

enable_secondary_routes = 0

"""
Si `enable_secondary_routes = 0`, les routes "secondaires" suivantes seront désactivées :

  - "/criteres_recruteurs/qualifications",
  - "/criteres_recruteurs/formations",
  - "/criteres_recruteurs/permis_conduire",
  - "/criteres_recruteurs/langues",

    (elles n'apportent pas d'information importante)
"""


def strip_accents(text):
    """
    Fonction qui remplace un char avec accent avec son équivalent sans accent.
    Sert ici pour pouvoir trier sans tenir compte des accents.
      (car "Île-de-France" est placé après "Occitanie" par exemple, mais on ne veut pas que ce soit le cas)
    """
    import unicodedata

    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")

    """
    Ainsi, on aura :

    print(
        strip_accents("Île-de-France"),  ##==> Ile-de-France (la fonction remplace les accents)
        strip_accents("Saint-Cyr-l'École"),  ##==> Saint-Cyr-l'Ecole
    )
    """


app = FastAPI(
    title="API sur les offres d'emploi chez France Travail",
    description=dedent("""
    - <u> Notes concernant les paramètres de localisation : </u>
      <br> <br>
      - Pour connaître `code_region`, `code_departement`, `code_postal` ou `code_insee`, lancer la requête associée sous le tag `{tag_location_mapping_name_code}`.
      <br> <br>
      - Un code postal peut avoir plusieurs code insee.
        - Par exemple le code postal 78310 est partagé entre la commune de Coignières (code insee 78168), et la commune de Maurepas (code insee 78383)."""),
    openapi_tags=[
        {
            "name": tag_all_offres,
            "description": "aaa",
        },
        # {
        #     "name": "Pour une offre d'emploi",
        #     "description": "aaa2",
        # },
        {
            "name": tag_location_mapping_name_code,
            "description": "Donne la correspondance entre le <b>nom</b> d'une région et son <b>code</b><br> &nbsp; (idem pour les départements, les villes et les communes)",
        },
    ],
    # pour désactiver la coloration syntaxique sinon dans une réponse de type text/plain, on peut avoir du blanc, du rouge, du vert, du orange suivant les chars...
    swagger_ui_parameters={"syntaxHighlight": False},  # https://fastapi.tiangolo.com/ru/how-to/configure-swagger-ui/#disable-syntax-highlighting
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
    dtype=str,  # toutes les colonnes à str
    # dtype={
    #     "code_insee": str,
    #     "nom_commune": str,
    #     "code_postal": str,
    #     "nom_ville": str,
    #     "code_departement": str,
    #     "nom_departement": str,
    #     "code_region": str,
    #     "nom_region": str,
    # },
)


# Fonction pour centraliser les filtres
def set_endpoints_filters(
    metier_data: Optional[str] = Query(
        default=None,
        description=dedent("""
        Filtrer sur les métiers "Data Engineer", "Data Analyst" ou "Data Scientist".\n
        &nbsp; <i> Valeurs possibles : `DE`, `DA` ou `DS` </i>"""),
    ),
    date_creation_min: Optional[str] = Query(
        default=None,
        description="Filtrer par date de création des offres (au format `YYYY-MM-DD`).  <br> &nbsp; <i> Par exemple, les offres à partir du `2025-04-28` </i>",
    ),
    code_region: Optional[List[str]] = Query(default=None, description="Filtrer sur le code de la région."),
    code_departement: Optional[List[str]] = Query(default=None, description="Filtrer sur le code du département."),
    code_postal: Optional[List[str]] = Query(default=None, description="Filtrer sur le code postal."),
    code_insee: Optional[List[str]] = Query(default=None, description="Filtrer sur le code insee."),
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
    if code_region:
        invalid_codes_region = [cr for cr in code_region if cr not in df_location["code_region"].values]
        if invalid_codes_region:
            raise HTTPException(status_code=400, detail=f"Les codes région {invalid_codes_region} sont invalides.")

    # Validation de `code_departement`
    if code_departement:
        invalid_codes_departement = [cd for cd in code_departement if cd not in df_location["code_departement"].values]
        if invalid_codes_departement:
            raise HTTPException(status_code=400, detail=f"Les codes département {invalid_codes_departement} sont invalides.")

    # Validation de `code_postal`
    if code_postal:
        invalid_codes_postal = [cp for cp in code_postal if cp not in df_location["code_postal"].values]
        if invalid_codes_postal:
            raise HTTPException(status_code=400, detail=f"Les codes postaux {invalid_codes_postal} sont invalides.")

    # Validation de `code_insee`
    if code_insee:
        invalid_codes_insee = [ci for ci in code_insee if ci not in df_location["code_insee"].values]
        if invalid_codes_insee:
            raise HTTPException(status_code=400, detail=f"Les codes insee {invalid_codes_insee} sont invalides.")

    return {
        "metier_data": metier_data,
        "date_creation_min": date_creation_min,
        "code_region": code_region,
        "code_departement": code_departement,
        "code_postal": code_postal,
        "code_insee": code_insee,
    }


# Fonction de filtrage qui modifie la requête SQL selon les paramètres
def execute_modified_sql_request_with_filters(
    sql_files_directory_part_2,
    metier_data,
    date_creation_min,
    code_region,
    code_departement,
    code_postal,
    code_insee,
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

        # Filtrage par "metier_data"
        if metier_data is None:
            sql_file_content = sql_file_content.replace("metier_data = 'placeholder_metier_data'", "1=1")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_metier_data'", "%s")

        # Filtrage par "date_creation_min"
        if date_creation_min is None:
            sql_file_content = sql_file_content.replace("AND date_creation >= 'placeholder_date_creation_min'", "")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_date_creation_min'", "%s")
            params.append(date_creation_min)

        # Filtrage par "code_region"
        if code_region is None:
            sql_file_content = sql_file_content.replace("AND code_region IN (placeholder_code_region)", "")
        else:
            placeholders = ", ".join(["%s"] * len(code_region))
            sql_file_content = sql_file_content.replace("placeholder_code_region", placeholders)
            params.extend(code_region)

        # Filtrage par "code_departement"
        if code_departement is None:
            sql_file_content = sql_file_content.replace("AND code_departement IN (placeholder_code_departement)", "")
        else:
            placeholders = ", ".join(["%s"] * len(code_departement))
            sql_file_content = sql_file_content.replace("placeholder_code_departement", placeholders)
            params.extend(code_departement)

        # Filtrage par "code_postal"
        if code_postal is None:
            sql_file_content = sql_file_content.replace("AND code_postal IN (placeholder_code_postal)", "")
        else:
            placeholders = ", ".join(["%s"] * len(code_postal))
            sql_file_content = sql_file_content.replace("placeholder_code_postal", placeholders)
            params.extend(code_postal)

        # Filtrage par "code_insee"
        if code_insee is None:
            sql_file_content = sql_file_content.replace("AND code_insee IN (placeholder_code_insee)", "")
        else:
            placeholders = ", ".join(["%s"] * len(code_insee))
            sql_file_content = sql_file_content.replace("placeholder_code_insee", placeholders)
            params.extend(code_insee)

        modified_sql_file_content = sql_file_content

        with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
            with conn.cursor() as cursor:
                print(f'\n{Fore.CYAN}===> Requête SQL depuis le fichier "{sql_files_directory_part_2}" :')
                print(f"{Style.DIM}{modified_sql_file_content}")
                print(f"{Fore.CYAN}===> paramètres :")
                print(f"{Fore.CYAN}{Style.DIM}{params}")

                cursor.execute(modified_sql_file_content, tuple(params))
                if fetch == "all":
                    return cursor.fetchall()
                elif fetch == "one":
                    return cursor.fetchone()


@app.get(
    "/statistiques/total_offres",
    tags=[tag_all_offres],
    summary="Nombre total d'offres d'emploi",
    description=message_on_endpoints_about_fields,
)
def get_number_of_offers(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("00_table_OffreEmploi", "total_offres.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="one")
    total_offres = result[0] if result else 0

    return Response(content=f"total: {total_offres:,} offres", media_type="text/plain")  # espace pour séparer les milliers


def replace_tab_by_space(text):
    """
    Cette mini fonction est utilisée pour remplacer les tabulations par des espaces normales,
     sinon on se retrouve lorsqu'on veut afficher un tableau avec des lignes inesthétiques de ce genre :

    +-----------------+--------+--------------------------------------------------------------+-----------------+
    |   nb occurences |   code | libelle                                                      | code exigence   |
    |-----------------+--------+--------------------------------------------------------------+-----------------|
    |               1 |        | Connaissances en base de données                             | E               |
    |               1 |        | Benchmark                                                    | E               |
    |               1 |        | -	Pratique C++,Python                                                              | E               |   <== pas esthétique
    |               1 |        | azure                                                        | E               |
    |               1 |        | -	Familier de Linux, QL, bus Can, windows visio                                                              | E               |   <== pas esthétique
    |               1 |        | Intégration et de déploiement continu                        | E               |
    |               1 |        | o	Parfaite connaissance du modèle OSI et particuli                                                              | E               |   <== pas esthétique
    |               1 |        | Scripting                                                    | E               |
    |               1 |        | PHP                                                          | E               |
    |               1 |        | Capacité d'analyse / Esprit de synthèse                      | E               |
    +-----------------+--------+--------------------------------------------------------------+-----------------+
    """
    import re

    return re.sub(r"[\t]+", " ", text)  # Remplace tabulations par un espace


@app.get(
    "/criteres_recruteurs/competences",
    tags=[tag_all_offres],
    summary="Compétences (techniques, managériales...) demandées par les recruteurs",
    description=dedent(f"""
    {message_on_endpoints_about_fields}

    <u> Tri : </u>
      - par code exigence (<b>E</b>xigé d'abord, puis <b>S</b>ouhaité), puis
      - par nombre d'occurences (DESC), puis
      - par code (ASC)

    """),
)
def get_competences(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("01_table_Competence", "competences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")

    truncated_result = [(row[0], row[1], replace_tab_by_space(row[2][:120]), row[3]) for row in result]

    table = tabulate(truncated_result, headers=["nb occurences", "code", "libelle", "code exigence"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get(
    "/criteres_recruteurs/experiences",
    tags=[tag_all_offres],
    summary="Expériences (études, diplôme, années expérience...) demandées par les recruteurs",
    description=dedent(f"""\
    {message_on_endpoints_about_fields}

    <u> Tri : </u>
      - par code exigence (<b>D</b>ébutant d'abord, <b>S</b>ouhaité, puis <b>E</b>xigé), puis
      - par nombre d'occurences (DESC), puis
      - par libellé (ASC).

    <u> Peut répondre aux questions : </u>
      - Nombre d'années d'études minimum ? Nombre d'années d'expérience minimum ?
      - Expérience requise dans tel domaine ou tel secteur ? Expérience requis sur un poste similaire ?
      - Est-ce qu'un diplôme est requis ? etc...
    """),
)
# Chaque champ est facultatif (champ vide = pas de filtre).
def get_experiences(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("02_table_Experience", "experiences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
    table = tabulate(result, headers=["nb occurences", "libelle", "commentaire", "code exigence"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get(
    "/criteres_recruteurs/qualites_professionnelles",
    tags=[tag_all_offres],
    summary="Qualités professionnelles demandées par les recruteurs",
    description=dedent(f"""\
    {message_on_endpoints_about_fields}

    <u> Tri :</u> par nombre d'occurences (DESC).
    """),
)
def get_qualites_professionnelles(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("03_table_QualiteProfessionnelle", "qualites_professionnelles.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
    table = tabulate(result, headers=["nb occurences", "qualité professionnelle"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get(
    "/mapping_geographique/region",
    tags=[tag_location_mapping_name_code],
    summary="Mapping entre le nom de la région et de son code",
)
def get_mapping_region():
    df_region = df_location[["nom_region", "code_region"]].drop_duplicates().copy()
    df_region["nom_region_sans_accent"] = df_region["nom_region"].apply(strip_accents)
    df_region_sorted = df_region.sort_values(by="nom_region_sans_accent")[["nom_region", "code_region"]]

    table = tabulate(df_region_sorted.values.tolist(), headers=["Nom région", "Code région"], tablefmt="psql")
    return Response(content=table, media_type="text/plain")


if enable_secondary_routes:

    @app.get(
        "/criteres_recruteurs/qualifications",
        tags=[tag_all_offres],
        summary="Niveaux de qualification professionnelle demandés par les recruteurs",
        description=dedent(f"""\
        {message_on_endpoints_about_fields}

        <u> Tri :</u> par nombre d'occurences (DESC).
        """),
    )
    def get_qualifications(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("04_table_Qualification", "qualifications.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "qualification"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/formations",
        tags=[tag_all_offres],
        summary="Formations (domaines, nombre d'années d'études) demandées par les recruteurs",
        description=dedent(f"""\
        {message_on_endpoints_about_fields}

        <u> Tri : </u>
          - par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis
          - par nombre d'occurences (DESC), puis
          - par code (ASC), puis
          - par niveau (ASC)
        """),
    )
    def get_formations(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("05_table_Formation", "formations.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "code", "domaine", "niveau", "commentaire", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/permis_conduire",
        tags=[tag_all_offres],
        summary="Permis de conduire demandés par les recruteurs",
        description=dedent(f"""\
        {message_on_endpoints_about_fields}

        <u> Tri : </u>
          - par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis
          - par nombre d'occurences (DESC), puis
          - par permis de conduire (ASC)
        """),
    )
    def get_permis_conduire(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("06_table_PermisConduire", "permis_conduire.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "permis de conduire", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/langues",
        tags=[tag_all_offres],
        summary="Langues demandées par les recruteurs",
        description=dedent(f"""\
        {message_on_endpoints_about_fields}

        <u> Tri : </u>
          - par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis
          - par nombre d'occurences (DESC), puis
          - par langue (ASC)
        """),
    )
    def get_permis_conduire(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("07_table_Langue", "langues.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "langue", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")
