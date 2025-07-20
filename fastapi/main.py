# cd fastapi/  &&  uvicorn main:app --reload
# cd fastapi/  &&  uvicorn main:app --reload  --log-level debug

import os

from enum import Enum
from textwrap import dedent  # pour gérer les indentations
from typing import List, Optional

import pandas as pd
import psycopg2

from colorama import Fore, Style, init  # todo : à supprimer ?
from tabulate import tabulate  # pour afficher les résultats sous forme de tableau

from fastapi import Depends, FastAPI, HTTPException, Query, Response  # status

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


tag_one_offer = "Pour une seule offre d'emploi"
tag_all_offers = "Pour toutes les offres d'emploi"
tag_location_mapping_name_code = 'Mapping "nom <> code" pour les régions, départements, villes et communes'

description_metier_data = 'Filtrer sur le métier "Data Engineer" `DE`, "Data Analyst" `DA` ou "Data Scientist `DS` (`--` pour ne pas filtrer sur ces métiers)'
description_offres_dispo_only = "`True` pour filtrer sur les offres disponibles uniquement (disponibles au jour où l'extraction des données a eu lieu), `False` sinon."
description_empty_field = "_(champ vide = pas de filtre)_"

enable_secondary_routes = 1

# valeurs définies dans le "docker-compose.yml"
psycopg2_connect_dict = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "database": os.getenv("DB_NAME", "francetravail"),
    "user": os.getenv("DB_USER", "mhh"),
    "password": os.getenv("DB_PASSWORD", "mhh"),
}

"""
Si `enable_secondary_routes = 0`, les routes "secondaires" suivantes seront désactivées :

  - "/criteres_recruteurs/qualifications",
  - "/criteres_recruteurs/formations",
  - "/criteres_recruteurs/permis_conduire",
  - "/criteres_recruteurs/langues",

    (elles n'apportent pas d'information importante, et polluent open api)
"""


###### définitions de mini fonctions()


def replace_tab_by_space(text):
    """
    Cette mini fonction est utilisée pour remplacer les tabulations par des espaces normales,
     sinon on se retrouve lorsqu'on veut afficher un tableau avec des lignes inesthétiques de ce genre :

    +-----------------+--------+--------------------------------------------------------------+-----------------+
    |   nb occurences |   code | libelle                                                      | code exigence   |
    |-----------------+--------+--------------------------------------------------------------+-----------------|
    |               1 |        | Connaissances en base de données                             | E               |
    |               1 |        | -	Pratique C++,Python                                                              | E               |   <== pas esthétique
    |               1 |        | -	Familier de Linux, QL, bus Can, windows visio                                                              | E               |   <== pas esthétique
    |               1 |        | Intégration et de déploiement continu                        | E               |
    |               1 |        | o	Parfaite connaissance du modèle OSI et particuli                                                              | E               |   <== pas esthétique
    |               1 |        | Scripting                                                    | E               |
    |               1 |        | PHP                                                          | E               |
    +-----------------+--------+--------------------------------------------------------------+-----------------+
    """
    import re

    return re.sub(r"[\t]+", " ", text)  # Remplace tabulations par un espace


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
    description=dedent(f"""
    - Notes concernant les paramètres de localisation `code_region`, `code_departement`, `code_postal` et `code_insee` :
      <br> <br>
      - Remplir ces champs est facultatif (pas de valeur = pas de filtre).
      <br>
      - Pour connaître les valeurs possibles, lancer la requête associée sous la partie `{tag_location_mapping_name_code}`.
      <br>
      - Un code postal peut avoir plusieurs codes insee (exemple : le <u>code postal 78310</u> est partagé entre la commune de Coignières (<u>code insee 78168</u>), et la commune de Maurepas (<u>code insee 78383</u>)).
      """),  # noqa
    openapi_tags=[
        {
            "name": tag_one_offer,
            "description": "à compléter plus tard",
        },
        {
            "name": tag_all_offers,
            "description": "à compléter plus tard",
        },
        {
            "name": tag_location_mapping_name_code,
            "description": "Correspondance entre le <b>nom</b> et le <b>code</b><br> d'une région, département, ville, commune",
        },
    ],
    # pour désactiver la coloration syntaxique sinon dans une réponse de type text/plain, on peut avoir du blanc, du rouge, du vert, du orange suivant les chars...
    swagger_ui_parameters={"syntaxHighlight": False},  # https://fastapi.tiangolo.com/ru/how-to/configure-swagger-ui/#disable-syntax-highlighting
)


sql_file_directory_part_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql_requests")

# DEFAULT_CSV_PATH : valeur par défaut si la variable d’environnement n’existe pas
DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "airflow",
    "data",
    "resources",
    "code_name__city_department_region.csv",
)

# variable "location_csv_file" écrasée par la valeur définie dans le Dockerfile si script exécuté dans le conteneur
location_csv_file = os.getenv("LOCATION_CSV_PATH", DEFAULT_CSV_PATH)

print(f"Chargement du fichier CSV depuis : {location_csv_file}")


df_location = pd.read_csv(location_csv_file, dtype=str)  # toutes les colonnes à str


class MetierDataEnum(str, Enum):
    DE = "DE"
    DA = "DA"
    DS = "DS"


# Fonction pour centraliser les filtres
def set_endpoints_filters(
    metier_data: Optional[MetierDataEnum] = Query(default=None, description=description_metier_data),
    offres_dispo_only: Optional[bool] = Query(default=False, description=description_offres_dispo_only),
    code_region: Optional[List[str]] = Query(default=None, description="Filtrer sur le code de la région."),
    code_departement: Optional[List[str]] = Query(default=None, description="Filtrer sur le code du département."),
    code_postal: Optional[List[str]] = Query(default=None, description="Filtrer sur le code postal."),
    code_insee: Optional[List[str]] = Query(default=None, description="Filtrer sur le code insee."),
):
    # Validation de `metier_data`
    allowed_metier_data = {"DE", "DA", "DS", None}  # set

    if metier_data not in allowed_metier_data:
        raise HTTPException(status_code=400, detail=f"'metier_data' doit être vide ou valoir 'DE', 'DA' ou 'DS'")

    # Validation de `offres_dispo_only`
    if offres_dispo_only not in (False, True):
        raise HTTPException(status_code=400, detail=f"'offres_dispo_only' doit être un booléen.")

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
        "offres_dispo_only": offres_dispo_only,
        "code_region": code_region,
        "code_departement": code_departement,
        "code_postal": code_postal,
        "code_insee": code_insee,
    }


# Fonction de filtrage qui modifie la requête SQL selon les paramètres
def execute_modified_sql_request_with_filters(
    sql_files_directory_part_2,
    metier_data,
    offres_dispo_only=False,
    code_region=None,
    code_departement=None,
    code_postal=None,
    code_insee=None,
    fetch="all",
):
    """
    Fonction utilisée pour les routes dont le tag est "tag_all_offers".

    Prend en entrée le fichier sql dont le chemin se termine par la paramètre "sql_files_directory_part_2"
      et applique les filtres en remplaçant les placeholders sur la requête SQL en fonction des paramètres fournis.

    Exécute le fichier sql modifié.
    """
    params = []

    with open(os.path.join(sql_file_directory_part_1, sql_files_directory_part_2), "r") as file:
        sql_file_content = file.read()

        # Filtrage par "metier_data"
        if metier_data is None:
            sql_file_content = sql_file_content.replace("metier_data = 'placeholder_metier_data'", "1=1")
        else:
            sql_file_content = sql_file_content.replace("'placeholder_metier_data'", "%s")
            params.append(metier_data)

        # Filtrage par "offres_dispo_only"
        if offres_dispo_only:
            pass  # On garde le CTE et le JOIN entouré par des commentaires tels quels
        else:
            # on commente (/* ... */) les parties suivantes :
            sql_file_content = sql_file_content.replace("-- ** BEGIN__TO_KEEP_OR_NOT_ON_FASTAPI", "/*").replace("-- ** END__TO_KEEP_OR_NOT_ON_FASTAPI", "*/")

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

        with psycopg2.connect(**psycopg2_connect_dict) as conn:
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


def set_endpoints_filters_2(
    offre_id: Optional[str] = Query(default="*joker*", description='"offre_id" sur 7 digits (laisser "*joker*" pour avoir une offre aléatoire'),
):
    if len(offre_id) != 7:
        raise HTTPException(status_code=400, detail=f"'offre_id' doit être sur 7 digits.")

    return offre_id


@app.get(
    "/offre/quelques_attributs_provenant_des_transformations",
    tags=[tag_one_offer],
    summary="Afficher quelques attributs issues des transformations",
)
def get_attributes_for_a_specific_offer(filters: str = Depends(set_endpoints_filters_2)):
    offre_id = filters

    # on choisit un offre_id parmi ceux existant (grâce au fichier créé par le "DAG 1", tâche "A11")
    if offre_id == "*joker*":
        offres_ids_list = []
        with open("offers_ids.txt", "r") as file:
            for line in file:
                line = line.strip()  # .strip() sinon on aura les retours à la ligne "\n"
                if line:  # pour prendre que les lignes avec du texte
                    offres_ids_list.append(line)

        import random

        offre_id = random.choice(offres_ids_list)

    sql_file_directory_part_2 = os.path.join("misc", "for_a_specific_offer.pgsql")
    with open(os.path.join(sql_file_directory_part_1, sql_file_directory_part_2), "r") as file:
        sql = file.read()
        params = (offre_id,)

        with psycopg2.connect(**psycopg2_connect_dict) as conn:
            with conn.cursor() as cursor:
                print(f'\n{Fore.CYAN}===> Requête SQL depuis le fichier "{sql_file_directory_part_2}" :')
                print(f"{Style.DIM}{sql}")

                cursor.execute(sql, params)

                return cursor.fetchone()


##########################


@app.get(
    "/stats/total_offres",
    tags=[tag_all_offers],
    summary="Nombre total d'offres d'emploi",
)
def get_number_of_offers(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("00_table_OffreEmploi", "total_offres.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="one")
    total_offres = result[0] if result else 0

    return Response(content=f"total: {total_offres:,} offres".replace(",", " "), media_type="text/plain")  # espace pour séparer les milliers


@app.get("/stats/classement/region", tags=[tag_all_offers], summary="Classement des régions qui recrutent le plus", description="<u> Tri :</u> par nombre d'offres (DESC).")
def get_regions_ranking(
    metier_data: Optional[MetierDataEnum] = Query(default=None, description=description_metier_data),
    offres_dispo_only: Optional[bool] = Query(default=False, description=description_offres_dispo_only),
):
    sql_file_directory_part_2 = os.path.join("08_table_Localisation", "classement_regions.pgsql")
    result = execute_modified_sql_request_with_filters(sql_files_directory_part_2=sql_file_directory_part_2, metier_data=metier_data, offres_dispo_only=offres_dispo_only, fetch="all")
    result = [(row[0], row[1].replace("pourcent", "%"), row[2]) for row in result]  # note : écrire % dans le fichier pgsql est problématique par rapport aux %s
    table = tabulate(result, headers=["nb offres", "pourcentage", "région"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get("/stats/classement/departement", tags=[tag_all_offers], summary="Classement des départements qui recrutent le plus (top 30)", description="<u> Tri :</u> par nombre d'offres (DESC).")
def get_departements_ranking(
    metier_data: Optional[MetierDataEnum] = Query(default=None, description=description_metier_data),
    offres_dispo_only: Optional[bool] = Query(default=False, description=description_offres_dispo_only),
):
    sql_file_directory_part_2 = os.path.join("08_table_Localisation", "classement_departements.pgsql")
    result = execute_modified_sql_request_with_filters(sql_files_directory_part_2=sql_file_directory_part_2, metier_data=metier_data, offres_dispo_only=offres_dispo_only, fetch="all")
    result = [(row[0], row[1].replace("pourcent", "%"), row[2]) for row in result]  # note : écrire % dans le fichier pgsql est problématique par rapport aux %s
    table = tabulate(result, headers=["nb offres", "pourcentage", "département"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get("/stats/classement/ville", tags=[tag_all_offers], summary="Classement des villes qui recrutent le plus (top 30)", description="<u> Tri :</u> par nombre d'offres (DESC).")
def get_villes_ranking(
    metier_data: Optional[MetierDataEnum] = Query(default=None, description=description_metier_data),
    offres_dispo_only: Optional[bool] = Query(default=False, description=description_offres_dispo_only),
):
    sql_file_directory_part_2 = os.path.join("08_table_Localisation", "classement_villes.pgsql")
    result = execute_modified_sql_request_with_filters(sql_files_directory_part_2=sql_file_directory_part_2, metier_data=metier_data, offres_dispo_only=offres_dispo_only, fetch="all")
    result = [(row[0], row[1].replace("pourcent", "%"), row[2]) for row in result]  # note : écrire % dans le fichier pgsql est problématique par rapport aux %s
    table = tabulate(result, headers=["nb offres", "pourcentage", "ville"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


##########################


@app.get(
    "/criteres_recruteurs/competences",
    tags=[tag_all_offers],
    summary="Compétences (techniques, managériales...) demandées par les recruteurs",
    description="<u> Tri :</u> <b>1/</b> par code exigence (<b>E</b>xigé d'abord, puis <b>S</b>ouhaité), puis <b>2/</b> par nombre d'occurences (DESC), puis <b>3/</b> par code (ASC).",
)
def get_competences(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("01_table_Competence", "competences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")

    truncated_result = [(row[0], row[1], replace_tab_by_space(row[2][:120]), row[3]) for row in result]

    table = tabulate(truncated_result, headers=["nb occurences", "code", "libelle", "code exigence"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get(
    "/criteres_recruteurs/experiences",
    tags=[tag_all_offers],
    summary="Expériences (études, diplôme, années expérience...) demandées par les recruteurs",
    description=dedent("""\
    <u> Tri :</u> <b>1/</b> par code exigence (<b>D</b>ébutant d'abord, <b>S</b>ouhaité, puis <b>E</b>xigé), puis <b>2/</b> par nombre d'occurences (DESC), puis <b>3/</b> par libellé (ASC).

    <u> Répond à :</u> Nombre d'années d'études ou d'expérience minimum ? Expérience requise dans tel domaine ou sur poste similaire ? Diplôme requis ? etc...
    """),
)
def get_experiences(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("02_table_Experience", "experiences.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
    table = tabulate(result, headers=["nb occurences", "libelle", "commentaire", "code exigence"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


@app.get(
    "/criteres_recruteurs/qualites_professionnelles",
    tags=[tag_all_offers],
    summary="Qualités professionnelles demandées par les recruteurs",
    description="<u> Tri :</u> par nombre d'occurences (DESC).",
)
def get_qualites_professionnelles(filters: dict = Depends(set_endpoints_filters)):
    sql_file_directory_part_2 = os.path.join("03_table_QualiteProfessionnelle", "qualites_professionnelles.pgsql")
    result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
    table = tabulate(result, headers=["nb occurences", "qualité professionnelle"], tablefmt="psql")

    return Response(content=table, media_type="text/plain")


##################################


def get_sorted_table_from_df(df, name, code):
    """
    Prend en entrée df_location, et deux de ses colonnes (nom+code) pour
     retourner un tableau affichable en mode text/plain en response body de fastapi.
    """
    df_copy = df[[name, code]].drop_duplicates().copy()
    df_copy["nom_sans_accent"] = df_copy[name].apply(strip_accents)

    # Forcer le code postal sur 5 digits pour avoir 02300 au lieu de 2300 (on a 2300 sur open api, mais pas en sortie de pandas et tabulate...)
    #  (pas de pb pour le code insee bizarrement)
    if code == "code_postal":
        df_copy[code] = df_copy[code].astype(str).str.zfill(5)

    df_sorted = df_copy.sort_values(by="nom_sans_accent")[[name, code]]

    return tabulate(df_sorted.values.tolist(), headers=[name, code], tablefmt="psql")


@app.get("/mapping_nom_code/region", tags=[tag_location_mapping_name_code], summary="Mapping entre le nom de la région et de son code")
def get_mapping_region():
    table = get_sorted_table_from_df(df_location, "nom_region", "code_region")
    return Response(content=table, media_type="text/plain")


@app.get("/mapping_nom_code/departement", tags=[tag_location_mapping_name_code], summary="Mapping entre le nom du département et de son code")
def get_mapping_departement():
    table = get_sorted_table_from_df(df_location, "nom_departement", "code_departement")
    return Response(content=table, media_type="text/plain")


@app.get("/mapping_nom_code/ville", tags=[tag_location_mapping_name_code], summary="Mapping entre le nom du ville et de son code")
def get_mapping_ville():
    table = get_sorted_table_from_df(df_location, "nom_ville", "code_postal")
    return Response(content=table, media_type="text/plain")


@app.get("/mapping_nom_code/commune", tags=[tag_location_mapping_name_code], summary="Mapping entre le nom de la commune et de son code")
def get_mapping_commune():
    table = get_sorted_table_from_df(df_location, "nom_commune", "code_insee")
    return Response(content=table, media_type="text/plain")


if enable_secondary_routes:

    @app.get(
        "/criteres_recruteurs/qualifications",
        tags=[tag_all_offers],
        summary="Niveaux de qualification professionnelle demandés par les recruteurs",
        description="<u> Tri :</u> par nombre d'occurences (DESC).",
    )
    def get_qualifications(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("04_table_Qualification", "qualifications.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "qualification"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/formations",
        tags=[tag_all_offers],
        summary="Formations (domaines, nombre d'années d'études) demandées par les recruteurs",
        description="<u> Tri :</u> <b>1/</b> par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis <b>2/</b> par nombre d'occurences (DESC), puis <b>3/</b> par code (ASC), puis <b>4/</b> par niveau (ASC).",  # noqa
    )
    def get_formations(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("05_table_Formation", "formations.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "code", "domaine", "niveau", "commentaire", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/permis_conduire",
        tags=[tag_all_offers],
        summary="Permis de conduire demandés par les recruteurs",
        description="<u> Tri :</u> <b>1/</b> par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis <b>2/</b> par nombre d'occurences (DESC), puis <b>3/</b> par permis de conduire (ASC).",
    )
    def get_permis_conduire(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("06_table_PermisConduire", "permis_conduire.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "permis de conduire", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")

    @app.get(
        "/criteres_recruteurs/langues",
        tags=[tag_all_offers],
        summary="Langues demandées par les recruteurs",
        description="<u> Tri :</u> <b>1/</b> par code exigence (<b>E</b>xigé puis <b>S</b>ouhaité), puis <b>2/</b> par nombre d'occurences (DESC), puis <b>3/</b> par langue (ASC).",
    )
    def get_permis_conduire(filters: dict = Depends(set_endpoints_filters)):
        sql_file_directory_part_2 = os.path.join("07_table_Langue", "langues.pgsql")
        result = execute_modified_sql_request_with_filters(sql_file_directory_part_2, **filters, fetch="all")
        table = tabulate(result, headers=["nb occurences", "langue", "code exigence"], tablefmt="psql")

        return Response(content=table, media_type="text/plain")
