import csv
import json
import logging
import os
import shutil
import time

from datetime import datetime, timedelta
from pathlib import Path

import unidecode

from airflow import DAG
from airflow.decorators import task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "..", "data", "resources")
OUTPUTS_DIR = os.path.join(CURRENT_DIR, "..", "data", "outputs")

DOWNLOADED_JSONS_FROM_API_DIR = os.path.join(OUTPUTS_DIR, "offres", "0--original_json_files_from_api")
AGGREGATED_JSON_DIR = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file")

CREDENTIAL_FILENAME = os.path.join(RESOURCES_DIR, "api_credentials.yml")
CODES_APPELLATION_FILENAME = os.path.join(RESOURCES_DIR, "code_appellation_libelle.yml")
LOCATION_CSV_FILENAME = os.path.join(RESOURCES_DIR, "code_name__city_department_region.csv")
AGGREGATED_JSON_FILENAME = "all_in_one.json"

SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/


@task(task_id="S1_delete_all_in_one_json")
def delete_all_in_one_json():
    """
    Simple fonction pour supprimer le fichier json "all_in_one.json" s'il existe.
    Normalement, il n'est pas censé exister sauf dans des cas où le DAG est échoué en cours de route.
    (si ce fichier est existant, on peut se retrouver avec 2 fichiers json
      dans le dossier  "1--generated_json_file", ce qui pose problème).
    """
    file_to_remove = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file", "all_in_one.json")
    try:
        os.remove(file_to_remove)
    except FileNotFoundError:
        print(f"Le fichier n'existe pas : {file_to_remove}")


def check_file_exists(file_path):
    """
    Vérifie la présence du fichier yaml "file_path".
      - Si True, on continue le DAG.
      - Sinon, on arrête le DAG avec une Exception.
    """
    if os.path.exists(file_path):
        print(f'Le fichier est bien présent ici : "{file_path}", on continue le DAG...')
    else:
        raise Exception(f"==> Le fichier yaml n'est pas présent dans ({file_path}). On arrête le DAG.")

    return None


@task(task_id="S1_check_csv_file_exists")
def check_csv_file_exists(file_path):
    return check_file_exists(file_path)


@task(task_id="S1_check_appellation_yaml_file_exists")
def check_appellations_yaml_file_exists(file_path):
    return check_file_exists(file_path)


@task(task_id="S1_check_credentials_yaml_file_exists")
def check_credentials_yaml_file_exists(file_path):
    return check_file_exists(file_path)


@task(task_id="S1_count_number_of_json_file")
def count_number_of_json_file(directory_path):
    """
    Compte le nombre de json dans "directory_path".
      - Si 0 ou 1, on continue le DAG.
      - Sinon, on arrête le DAG avec une Exception.
    """
    json_files = [f for f in os.listdir(directory_path) if f.endswith(".json")]
    count = len(json_files)
    print(f'==> {count} fichier json dans "{directory_path}"')

    if count <= 1:
        print("0 ou 1 fichier json, on continue le DAG...")
    else:
        raise Exception(f"==> Au moins 2 fichiers json ({count} fichiers : {json_files}). On arrête le DAG.")

    return count


@task(task_id="S2_remove_all_json_files")
def remove_all_json_files(json_files_directory):
    """
    Supprime tous les fichiers json du dossier spécifié
    """

    for file in os.listdir(json_files_directory):
        json_to_delete = os.path.join(json_files_directory, file)

        # Vérifie si c'est un fichier et si son extension est .json
        if os.path.isfile(json_to_delete) and file.endswith(".json"):
            try:
                os.remove(json_to_delete)
            except Exception as e:
                print(f"Erreur lors de la suppression de {json_to_delete}: {e}")

    json_files = [f for f in os.listdir(json_files_directory) if f.endswith(".json")]
    count = len(json_files)

    if count == 0:
        print(f"Après suppression, il reste {count} fichiers (OK).")
    else:
        raise Exception(f'Il reste au moins un fichier json dans le dossier "{json_files_directory}"')

    return None


@task(task_id="S2_load_appellations_yaml_file")
def load_code_appellation_yaml_file():
    """
    Charge le fichier dans "Job_Market/airflow/data/resources/code_appellation_libelle.yml"
    Retourne une liste de dictionnaire de la forme :
      [
        {'code': '404278', 'libelle': 'Data_Engineer'},
        {'code': '404284', 'libelle': 'Ingenieur_Donnees'},
        {},
        ...
      ]
    """

    import yaml

    codes_appellation_filename = os.path.join(RESOURCES_DIR, "code_appellation_libelle.yml")

    with open(codes_appellation_filename, "r") as file:
        content = yaml.safe_load(file)
        code_libelle_list = content["code_appellation_libelle"]

    return code_libelle_list


@task(task_id="S2_get_creds_from_yaml_file")
def get_creds_from_yaml_file(file_path):
    """
    Récupération des credentials données sur le site de FT depuis un fichier yaml
    Retourne un dictionnaire utile pour la fonction "get_bearer_token()"
    """

    import yaml

    with open(file_path, "r") as file:
        creds = yaml.safe_load(file)

    identifiant_client = creds["FRANCE_TRAVAIL_API_CREDENTIALS"]["IDENTIFIANT_CLIENT"]
    cle_secrete = creds["FRANCE_TRAVAIL_API_CREDENTIALS"]["CLE_SECRETE"]

    dict_ = {"identifiant_client": identifiant_client, "cle_secrete": cle_secrete}

    return dict_


@task(task_id="S2_get_token")
def get_bearer_token(dict_, scope):
    """
    Récupère un Bearer Token grâce à l'API de France Travail.

    Paramètres :
    - dict_ : ce que renvoie "get_creds_from_yaml_file()", par exemple : {"identifiant_client": "xxxxxxx", "cle_secrete": "yyyyyyyyyyyy"}
    - scope (str) : Liste des scopes séparés par des espaces, indiquant les permissions demandées.

    Retourne :
    - Bearer Token (str) : pour l'authentification des requêtes, ou None en cas d'erreur.
    """

    import requests

    print(f'\n==> Fonction "get_bearer_token()"\n')

    # paramètres décrits ici https://francetravail.io/produits-partages/documentation/utilisation-api-france-travail/generer-access-token
    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    params = {"realm": "/partenaire"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    client_id = dict_["identifiant_client"]
    client_secret = dict_["cle_secrete"]

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    }

    response = requests.post(url, headers=headers, params=params, data=data)

    if response.status_code == 200:
        response_json = response.json()
        bearer_token = response_json["access_token"]
        print(f"Status Code: {response.status_code}, bearer token: {bearer_token}\n")
        return bearer_token
    else:
        print(f"Erreur, Status Code: {response.status_code}\n")
        print(f"=> {response.json()}")
        return None


@task(task_id="A1_get_offers")
def get_offers(token, code_libelle_list):
    """
    Récupére les offres de chaque appellation et les écrit dans un fichier json à partir des appellations ROME décrites dans "code_appellation_libelle.yml"
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150.
    A noter qu'on a droit à 10 maximum par seconde (sinon erreur 429 ("too much requests")).

    Ne retourne rien.
    """
    import requests

    def throttled_get(url, headers=None, params=None, max_retries=10, retry_delay=2):
        """
        Fonction utile pour la fonction get_offres().

        Effectue une requête GET avec gestion des erreurs de Status Code "429" ("too much requests").
        Réessaie jusqu'à "max_retries" fois avec un délai "retry_delay" entre chaque tentative.

        Paramètres :
        - "url" : URL de l'API
        - "headers" : dictionnaire d'en-têtes HTTP
        - "params" : dictionnaire de paramètres GET
        - "max_retries" : nombre maximum de tentatives
        - "retry_delay" : délai entre chaque tentative en secondes

        Retourne la réponse de la requête.

        Notes :
        - L'erreur "429" arrive assez fréquemment avec la parallélisation des tâches avec Airflow.
        - Terme "thottled" car exprime la régulation des requêtes.
        """

        for attempt in range(1, max_retries + 1):
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 429:
                return response

            print(f"[safe_get] Erreur 429 — tentative {attempt}/{max_retries}, pause {retry_delay}s...")
            time.sleep(retry_delay)

        raise Exception(f"[safe_get] Échec après {max_retries} tentatives : erreur 429 persistante...")

    code_appellation = code_libelle_list["code"]
    libelle = code_libelle_list["libelle"]

    output_file = os.path.join(OUTPUTS_DIR, "offres", "0--original_json_files_from_api", f"{code_appellation}_{libelle}.json")

    if os.path.exists(output_file):
        os.remove(output_file)

    offers_data = []

    print(f"== Récupération des offres ({code_appellation}: {libelle}) :")

    #### Première requête pour voir combien d'offres sont disponibles

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    params = {"appellation": code_appellation, "paysContinent": "01"}

    response = throttled_get(url, headers=headers, params=params, max_retries=10, retry_delay=2)

    print(f"==== Récupération des offres (requête 0), pour connaître le nombre d'offres :", end=" ")

    # print(response, int(response.headers.get("Content-Range").split("/")[-1]))  # pour investigation
    # print(response.headers.get("Content-Range"))  # exemple : "offres 0-0/9848"  # pour investigation

    max_offres = 0

    if response.status_code in [200, 206]:
        content_range = response.headers.get("Content-Range")
        if content_range is not None:
            max_offres = int(content_range.split("/")[-1])

    ###### réponse 200 : on peut déjà récupérer toutes les offres disponibles
    if response.status_code == 200:
        print(f"Status Code: {response.status_code}")
        # print(response.headers.get("Content-Range"))
        print(f"  => [{max_offres}] offres au total --> écriture dans le fichier")

        document_id = 0

        for obj in response.json()["resultats"]:
            offers_data.append(obj)
            document_id += 1

    ###### réponse 206 : on doit faire plusieurs requêtes pour récupérer tous les documents (limité à 3150 documents)
    elif response.status_code == 206:
        print(f"Status Code: {response.status_code} (Réponse partielle)")
        # print(response.headers.get("Content-Range"))
        print(f"  => [{max_offres}] offres au total")
        print(f"  => [{int(max_offres/150)+1}] requêtes nécessaires (avec 150 documents) pour tout récupérer", end="")
        print(f"  (limité à 21 requêtes, soit 3150 offres maximum)")  # (voir limitation du paramètre range)

        range_start = 0
        range_end = 149
        request_id = 1
        params["range"] = f"{range_start}-{range_end}"

        document_id = 0

        for _ in range(int(max_offres / 150) + 1):
            print(f"==== Récupération des offres (requête {request_id}) :", end=" ")
            response = throttled_get(url, headers=headers, params=params, max_retries=10, retry_delay=2)

            if response.status_code == 206:
                print(f"Status Code: {response.status_code}", end=", ")

                for obj in response.json()["resultats"]:
                    offers_data.append(obj)
                    document_id += 1
                print(f"{range_start}-{range_end}/{max_offres} --> écriture dans le fichier (total: {document_id})")

            else:
                """
                Par exemple si : (204) "No Content successful", (400) "La position de début doit être inférieure ou égale à 3000.",
                  (500) "Erreur technique. Veuillez contacter le support de francetravail.io."
                """
                try:
                    print(f"Status Code: {response.status_code} ==> {response.json()}")
                except requests.exceptions.JSONDecodeError:  # cas où "response.json()" renvoie "requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
                    print(f"Status Code: {response.status_code} ==> {response.text}")

                break

            range_start += 150
            range_end += 150
            params["range"] = f"{range_start}-{range_end}"
            request_id += 1

            # if request_id == 2:  # utile si besoin investigation
            #     break

    ###### autres cas
    else:
        try:
            print(f"Status Code: {response.status_code} ==> {response.json()}")
        except requests.exceptions.JSONDecodeError:  # cas où "response.json()" renvoie "requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
            print(f"Status Code: {response.status_code} ==> {response.text}")

    print("")

    ###### fin des requêtes, on écrit dans un .json et on vérifie que celui-ci est bien valide

    # écriture du fichier avec toutes les données
    with open(output_file, "w") as f:
        json.dump(offers_data, f, ensure_ascii=False, indent=4)

    # renommer le fichier json en ajoutant le nombre d'offres dans le nom du json
    dir_path, file_name = os.path.split(output_file)  # séparer le chemin et le nom du fichier
    new_file_name = f"{file_name[:-5]}__{document_id}_offres.json"
    # print(dir_path, file_name, new_file_name, sep="\n")  # utile si investigation
    new_file_path = os.path.join(dir_path, new_file_name)  # créer le chemin complet du nouveau fichier
    os.rename(output_file, new_file_path)  # renommer le fichier

    # ouvrir le fichier json valide pour vérifier qu'il est bien valide
    with open(new_file_path, "r") as valid:
        valid_content = valid.read()
        try:
            json.loads(valid_content)
            print("Le json est bien valide.")
        except json.JSONDecodeError as e:
            print(f"Le json n'est pas valide :\n==> {e}")

    return None


@task(task_id="A2_all_json_in_one")
def concatenate_all_json_into_one(downloaded_jsons_from_api_directory, aggregated_json_directory, new_json_filename):
    """
    On obtient suite à l'exécution de `get_offres()` x fichiers json (x = nombre d'appellations présents dans "code_appellation_libelle.yml").
    Cette présente fonction écrit dans un nouveau json tous les documents json de chaque fichier présent dans le dossier "downloaded_jsons_from_api_directory", en supprimant les doublons.

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """
    import pandas as pd

    print(f'\n==> Fonction "concatenate_all_into_one()"\n')

    df_concat = pd.DataFrame()

    for filename in os.listdir(downloaded_jsons_from_api_directory):
        if filename.endswith(".json"):  # and filename != concat_json_filename:  # traite aussi le cas du fichier sans extension
            print(filename)
            try:
                # si le json est bien valide
                with open(os.path.join(downloaded_jsons_from_api_directory, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df_concat = pd.concat([df_concat, df], ignore_index=True)

            except json.JSONDecodeError as e:
                print(f"Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
            except FileNotFoundError:
                print(f'Le fichier "{filename}" n\'a pas été trouvé.')
            except Exception as e:
                print(f"Une erreur inattendue s'est produite : {e}")

    num_offres_without_duplicates = len(df_concat.drop_duplicates(["id"]))
    print(f"\n --> df_concat : {df_concat.shape[0]} offres, df_concat_drop_duplicates : {num_offres_without_duplicates} offres\n\n")

    df_concat.drop_duplicates(["id"]).to_json(
        os.path.join(aggregated_json_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs (on les supprimera à la fin du DAG)

    # print(df_concat)  # pour investigation

    return new_json_filename


@task(task_id="A3_only_metropole")
def keep_only_offres_from_metropole(aggregated_json_directory, json_filename, new_json_filename):
    """
    Cette fonction écrase le json entré en paramètre, en ne conservant que les offres d'emploi de la France Métropolitaine.
    Elle ne conserve pas les offres de la Corse ni des DOMTOM.

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
     et aussi le nombre de ligne du DataFrame (si on en a besoin pour renommer le fichier, mais on ne le fera pas conformément au workflow)
    """

    import pandas as pd

    print(f'\n==> Fonction "keep_only_offres_from_metropole()"\n')

    df = pd.read_json(
        os.path.join(aggregated_json_directory, json_filename),
        dtype=False,  # pour ne pas inférer les dtypes
    )

    # lieuTravail est une colonne avec un dictionnaire, donc on utilise .json_normalize() pour avoir x colonnes pour chaque clé du dictionnaire.
    lieuTravail_normalized = pd.json_normalize(df["lieuTravail"])
    df_join = df.join(lieuTravail_normalized)
    df_lieu_norm = df_join[["id", "intitule"] + list(lieuTravail_normalized.columns)]

    # On exclut les offres où le libelle du lieu matche la regex suivante :
    df_lieu_norm_metropole = df_lieu_norm[~df_lieu_norm.libelle.str.match(r"^(\d{3}|2(A|B))\s-\s")]

    # On exclut les offres où le libelle du lieu matche un des départements suivants
    list_regions = [
        "Guadeloupe",
        "Martinique",
        "Guyane",
        "La Réunion",
        "Mayotte",
        "Collectivités d'Outre-Mer",
        "Saint-Pierre-et-Miquelon",
        "Saint-Barthélemy",
        "Saint-Martin",
        "Wallis-et-Futuna",
        "Polynésie française",
        "Nouvelle-Calédonie",
        "Haute-Corse",
        "Corse-du-Sud",
        "Corse",
        # "Nouvelle-Aquitaine",  # pour tester
    ]

    df_lieu_norm_metropole = df_lieu_norm_metropole[~df_lieu_norm_metropole["libelle"].isin(list_regions)]  # .value_counts(subset="libelle")

    # On réécrit un nouveau json avec uniquement les offres en métropole
    df_only_metropole = df[df["id"].isin(df_lieu_norm_metropole["id"])]

    df_only_metropole.to_json(
        os.path.join(aggregated_json_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs (on les supprimera à la fin du DAG)

    return new_json_filename, len(df_only_metropole)


@task(task_id="A4_add_location_attrs")
def add_location_attributes(aggregated_json_directory, json_filename, new_json_filename):
    """
    Prend en entrée un fichier json généré avec les fonctions précédentes.
    Génère en sortie un fichier json avec en plus les nouveaux attributs suivants :

        - code_insee
        - nom_commune
        - code_postal
        - nom_ville
        - code_departement
        - nom_departement
        - code_region
        - nom_region

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """

    import numpy as np
    import pandas as pd

    from geopy.geocoders import Nominatim

    print(f'\n==> Fonction "add_location_attributes()"\n')

    #### Chargement des fichiers

    print(f"\n====> Chargement des fichiers\n")

    df = pd.read_json(
        os.path.join(aggregated_json_directory, json_filename),
        dtype=False,  # désactiver l'inférence des types
    )

    df_insee = pd.read_csv(
        os.path.join(os.path.join(RESOURCES_DIR, "code_name__city_department_region.csv")),
        dtype=str,
    )

    lieuTravail_normalized = pd.json_normalize(df["lieuTravail"])
    df = df.join(lieuTravail_normalized)
    df_lieu = df[["id", "intitule"] + list(lieuTravail_normalized.columns)]

    df_lieu = df_lieu.rename(
        {
            "codePostal": "code_postal",
            "commune": "code_insee",
        },
        axis=1,
    )

    #### Cas_1 : "code_insee" renseigné

    # note : si commune = NAN, alors code_postal = NAN

    print(f'\n====> Cas_1 : "code_insee" renseigné\n')

    cas_1 = df_lieu[~df_lieu.code_insee.isna()]

    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_1.id), "lieu_cas"] = "cas_1"

    ### Ajout attributs ville/département/région

    df_insee_cas_1 = df_insee[["code_insee", "nom_commune", "nom_ville", "code_departement", "nom_departement", "code_region", "nom_region"]].drop_duplicates()
    df_lieu = df_lieu.merge(df_insee_cas_1, on="code_insee", how="left")

    # notes :
    #   - "left" car sinon "inner" va supprimer les lignes où "code_insee = code_postal = NAN"
    #   - on ne merge pas sur "on=["code_insee", "code_postal"]" car il y a un risque que ca matche pour "code_insee" mais pas pour "code_postal"
    #      (vu sur une offre (187TBCN) sur les 12 118 offres)

    ### Vérification

    # On vérifie que parmi les offres "cas_1", il n'y a pas de nom_ville à Nan.
    print(f'      Vérification cas_1 OK ? {len(df_lieu[(df_lieu.lieu_cas == "cas_1") & (df_lieu.nom_ville.isna())]) == 0}')

    # assert len(df_lieu[(df_lieu.lieu_cas == "cas_1") & (df_lieu.nom_ville.isna())]) == 0

    #### Cas_2 : "code_insee = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées

    print(f'\n====> Cas_2 : "code_insee = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées\n')

    # Récupération code_postal avec geopy

    geolocator = Nominatim(user_agent="my_geopy_app", timeout=10)  # timeout=1 par défaut
    # Notes :
    #   - La tâche Airflow essaie de faire beaucoup de requêtes HTTP consécutives au service "Nominatim", ce qui peut amener à l'erreur :
    #       ReadTimeoutError("HTTPSConnectionPool(host='nominatim.openstreetmap.org', port=443): Read timed out. (read timeout=1)")
    #   - Donc on contourne en mettant "timeout=10".

    latitude_min = 42.3328  # Sud
    latitude_max = 51.0892  # Nord
    longitude_min = -4.7956  # Ouest
    longitude_max = 8.2306  # Est

    def check_and_swap(row, max_retries=3, retry_delay=2):
        """
        Fonction pour inverser la latitude et la longitude si la latitude est hors de la fourchette.
        Réessaie plusieurs fois en cas d'erreur lors du géocodage.
        """

        # Vérification et inversion si nécessaire
        if row["latitude"] < latitude_min or row["latitude"] > latitude_max:
            row["latitude"], row["longitude"] = row["longitude"], row["latitude"]

        # Attribution de lieu_cas
        if (latitude_min <= row["latitude"] <= latitude_max) and (longitude_min <= row["longitude"] <= longitude_max):
            row["lieu_cas"] = "cas_2"
        else:
            # par exemple pour "id": "4016067"
            #  => "lieuTravail": { "libelle": "Corse", "latitude": 41.952873, "longitude": 8.795956 },
            row["lieu_cas"] = "cas_2_hors_metropole"

        # Géocodage avec retry
        retries = 0
        while retries < max_retries:
            try:
                location = geolocator.reverse((row["latitude"], row["longitude"]), language="fr", exactly_one=True)
                if location:
                    address = location.raw.get("address", {})
                    row["code_postal"] = address.get("postcode", "Inconnu")
                    print(f"  --> offre {row['id']} : coordonnées gps {row['latitude']}, {row['longitude']} ==> code postal trouvée : {row['code_postal']}")
                else:
                    row["code_postal"] = "Inconnu"
                    print(f"  --> offre {row['id']} : coordonnées gps {row['latitude']}, {row['longitude']} ==> code postal NON trouvée")
                break  # on sort de la boucle si succès

            except Exception as e:
                retries += 1
                print(f"Erreur pour ({row['latitude']}, {row['longitude']}), tentative {retries}/{max_retries}: {e}\n")
                # exemple de print :
                #  Erreur pour (48.896069, 2.206713), tentative 1/3: HTTPSConnectionPool(host='nominatim.openstreetmap.org', port=443):
                #  Max retries exceeded with url: /reverse?lat=48.896069&lon=2.206713&format=json&accept-language=fr&addressdetails=1
                #  (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fa961db0410>:
                #   Failed to establish a new connection: [Errno 101] Network is unreachable'))
                if retries < max_retries:
                    time.sleep(retry_delay)
                else:
                    row["code_postal"] = "Erreur geocodage"

        return row

    # /!\ temps d'exécution de plusieurs minutes
    cas_2 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1"])  # != cas_1
        & ~df_lieu.latitude.isna()
    ].apply(check_and_swap, axis=1)

    # Merge df_geopy et df_insee

    cas_2_geopy = cas_2.copy()

    # avant de merger avec df_insee, on supprime les colonnes qui n'ont que des NAN
    cas_2_geopy = cas_2_geopy.drop(["code_insee", "nom_commune", "nom_ville", "code_departement", "nom_departement", "code_region", "nom_region"], axis=1)

    cas_2_geopy_merge = cas_2_geopy.merge(df_insee, on="code_postal", how="left").drop_duplicates("id")

    # Gestion des cas où code_postal non reconnu

    # Parfois le code postal retourné par geopy n'est pas présent dans le fichier "code_name__city_department_region"
    # Dans ce cas, on va prendre les 2 premiers digits du code postal pour avoir le département, et récupérer la région.

    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge[cas_2_geopy_merge.code_insee.isna()]

    # Les 2 premiers digits du CP pour le code_departement.
    cas_2_geopy_merge_unknown_CP.loc[:, "code_departement"] = cas_2_geopy_merge_unknown_CP["code_postal"].apply(lambda x: x[:2])

    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge_unknown_CP.drop(["code_insee", "nom_commune", "nom_ville", "nom_departement", "code_region", "nom_region"], axis=1)  # avec le code_departement

    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge_unknown_CP.merge(df_insee[["code_departement", "nom_departement", "code_region", "nom_region"]], on="code_departement").drop_duplicates("id")

    # Update df

    # Modification pour avoir id en tant qu'index, nécessaire pour que .update() fonctionne (car .update() ne fonctionne que sur l'index du df)
    cas_2_geopy_merge.set_index("id", inplace=True)
    cas_2_geopy_merge_unknown_CP.set_index("id", inplace=True)

    cas_2_geopy_merge.update(cas_2_geopy_merge_unknown_CP)
    cas_2_geopy_merge.reset_index(inplace=True)

    # Update de df_lieu avec cas_2_geopy_merge

    # Modification pour avoir id en tant qu'index, nécessaire pour que .update() fonctionne (car .update() ne fonctionne que sur l'index du df)
    cas_2_geopy_merge.set_index("id", inplace=True)
    df_lieu.set_index("id", inplace=True)
    df_lieu.update(cas_2_geopy_merge)
    df_lieu.reset_index(inplace=True)

    # Vérification

    print(f'      Vérification cas_2 OK ? {len(df_lieu[(df_lieu.lieu_cas == "cas_2") & (df_lieu.nom_departement.isna())]) == 0}')

    # assert len(df_lieu[(df_lieu.lieu_cas == "cas_2") & (df_lieu.nom_departement.isna())]) == 0

    #### Cas_3 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = 'numéro_département - nom_département'" </u>

    print(f'\n====> Cas_3 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = numéro_département - nom_département"\n')

    cas_3 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1", "cas_2"])  # != cas_1/2
        & df_lieu.libelle.str.match(r"^\d{2}\s-\s")
    ]

    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_3.id), "lieu_cas"] = "cas_3"

    # Ajout attributs ville/département/région

    df_lieu.loc[df_lieu.lieu_cas == "cas_3", "code_departement"] = df_lieu.loc[df_lieu.lieu_cas == "cas_3", "libelle"].apply(lambda x: x.split(" - ")[0])

    # Update de df_lieu

    df_insee_cas_3 = df_insee[["code_departement", "nom_departement", "code_region", "nom_region"]].drop_duplicates()

    # récupération des noms de colonnes de df_lieu pour restaurer l'ordre des colonnes après .reset_index()
    columns_order = df_lieu.columns

    df_lieu.set_index("code_departement", inplace=True)
    df_insee_cas_3.set_index("code_departement", inplace=True)

    df_lieu.update(df_insee_cas_3)

    df_lieu.reset_index(inplace=True)

    df_lieu = df_lieu[columns_order]

    # Vérification

    print(f'      Vérification cas_3 OK ? {len(df_lieu[(df_lieu.lieu_cas == "cas_3") & (df_lieu.nom_departement.isna())]) == 0}')

    # assert len(df_lieu[(df_lieu.lieu_cas == "cas_3") & (df_lieu.nom_departement.isna())]) == 0

    #### Cas_4 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = nom_région"

    print(f'\n====> Cas_4 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = nom_région"\n')

    cas_4 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3"])  # != cas_1/2/3
        & ~df_lieu.libelle.isin(["FRANCE", "France", "France entière"])
    ]

    # cas_4.value_counts("libelle")
    # note:
    # Ile-de-France                 23   <=== i sans accent circonflexe
    # Île-de-France                  4   <=== i accent circonflexe
    # =>

    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_4.id), "lieu_cas"] = "cas_4"

    # Ajout attributs ville/département/région

    # Avant d'appliquer .update() :
    #
    # - On met le nom des régions de la colonne "libelle" en minuscule.
    # - On remplace les tirets par des espaces.
    # - On enlève les accents avec la lib unidecode

    df_lieu.loc[:, "libelle_traite"] = df_lieu["libelle"]

    df_lieu.loc[df_lieu.lieu_cas == "cas_4", "libelle_traite"] = df_lieu.loc[df_lieu.lieu_cas == "cas_4", "libelle"].apply(lambda x: unidecode.unidecode(x).lower().replace("-", " "))  # , axis=1)

    df_lieu[df_lieu.lieu_cas == "cas_4"]

    df_insee_cas_4_update_1 = df_insee.copy()

    df_insee_cas_4_update_1.nom_region = df_insee.nom_region.apply(lambda x: unidecode.unidecode(x).lower().replace("-", " "))

    df_insee_cas_4_update_1 = df_insee_cas_4_update_1[["code_region", "nom_region"]].drop_duplicates()

    df_insee_cas_4_update_1.rename({"nom_region": "libelle_traite"}, axis=1, inplace=True)  # pour pouvoir faire le .update()

    # Update 1

    df_lieu.set_index("libelle_traite", inplace=True)

    df_insee_cas_4_update_1.set_index("libelle_traite", inplace=True)

    df_lieu.update(df_insee_cas_4_update_1)

    # Update 2

    df_lieu.set_index("code_region", inplace=True)

    df_insee_cas_4_update_2 = df_insee.copy()

    df_insee_cas_4_update_2 = df_insee_cas_4_update_2[["code_region", "nom_region"]].drop_duplicates()

    df_insee_cas_4_update_2.set_index("code_region", inplace=True)

    df_lieu.update(df_insee_cas_4_update_2)

    df_lieu.reset_index(inplace=True)

    df_lieu = df_lieu[columns_order]

    # Vérification

    print(f'      Vérification cas_4 OK ? {len(df_lieu[(df_lieu.lieu_cas == "cas_3") & (df_lieu.nom_region.isna())]) == 0}')

    # assert len(df_lieu[(df_lieu.lieu_cas == "cas_4") & (df_lieu.nom_region.isna())]) == 0

    #### Cas_5 : "code_postal = code_insee = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"

    print(f'\n====> Cas_5 : "code_postal = code_insee = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"\n')

    cas_5 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3", "cas_4"])  # != cas_1/2/3/4
        & df_lieu.libelle.isin(["FRANCE", "France", "France entière"])
    ]

    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_5.id), "lieu_cas"] = "cas_5"

    # On remplace ["FRANCE", "France", "France entière"] par NaN
    df_lieu.loc[df_lieu.lieu_cas == "cas_5", "libelle"] = np.nan

    # Dans de rare cas, CP setté à "Inconnu" précédemment
    df_lieu.loc[df_lieu.lieu_cas == "cas_5", "code_postal"] = np.nan

    # Vérification qu'il n'y a pas d'autres cas que les cas 1, 2, 3, 4 et 5.

    print(f'      Vérification cas_5 OK ? {len(df_lieu[~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3", "cas_4", "cas_5"])]) == 0}\n\n')

    # assert len(df_lieu[~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3", "cas_4", "cas_5"])]) == 0  # != cas_1/2/3/4/5

    #### Update du df initial avec df_lieu

    # A la base, avec "df", on a pour l'attribut "lieuTravail"	les attributs suivants :
    # - libelle
    # - latitude
    # - longitude
    # - code_postal
    # - code_insee
    #
    #
    # Au final, on ne conservera que les attributs suivants qui proviennent de "df_lieu" :
    #
    # - code_postal
    # - nom_ville
    # - code_insee
    # - nom_commune
    # - code_departement
    # - nom_departement
    # - code_region
    # - nom_region

    # On supprime "intitule" car il est déjà dans le Dataframe "df", et "libelle"/"latitude"/"longitude" qui ne nous intéressent plus
    df_lieu = df_lieu.drop(["intitule", "libelle", "latitude", "longitude"], axis=1)

    # On ordonne les colonnes pour avoir un ordre plus logique (du plus spécifique au moins spécifique)
    df_lieu = df_lieu[
        [
            "id",
            "lieu_cas",
            "code_insee",
            "nom_commune",
            "code_postal",
            "nom_ville",
            "code_departement",
            "nom_departement",
            "code_region",
            "nom_region",
        ]
    ]

    # On supprime la colonne "lieuTravail" qui ne nous intéresse plus dorénavant, et les attributs de cette colonne
    df = df.drop(["lieuTravail", "libelle", "latitude", "longitude", "codePostal", "commune"], axis=1)

    df_final = pd.merge(left=df, right=df_lieu, on="id")

    #### Ecriture dans un fichier .json

    df_final.to_json(
        os.path.join(aggregated_json_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs (on les supprimera à la fin du DAG)

    return new_json_filename


@task(task_id="A5_add_dateExtraction_attr")
def add_date_extract_attribute(aggregated_json_directory, json_filename, new_json_filename, date_to_insert=None):
    """
    Fonction qui charge le json et qui écrit dans un nouveau json : un nouvel attribut "date_extraction" avec la date désirée
      (par défaut la date système pour avoir la date du jour)

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """

    import pandas as pd

    print(f'\n==> Fonction "add_date_extract_attribute()"\n')

    if date_to_insert is None:
        # date_to_insert = datetime.today().date()  # .date() pour ne pas avoir l'heure
        date_to_insert = datetime.today().strftime("%Y-%m-%d")  # formatage en string 'YYYY-MM-DD'

    df = pd.read_json(
        os.path.join(aggregated_json_directory, json_filename),
        dtype=False,  # pour ne pas inférer les dtypes
    )

    df["dateExtraction"] = pd.to_datetime(date_to_insert)  # sans la ligne suivante, on aura un timestamp en sortie de json "1743292800000"
    df["dateExtraction"] = df["dateExtraction"].dt.strftime("%Y-%m-%d")  # Formate les dates au format string 'YYYY-MM-DD'

    df.to_json(
        os.path.join(aggregated_json_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs (on les supprimera à la fin du DAG)
    # print(df)  # pour investigation

    return new_json_filename


@task.branch(task_id="A6_0_or_1_json_on_setup")
def nb_json_on_setup_0_or_1(count):
    # print(count)  # pour investigation
    if count == 0:  # si 0 fichier json
        # print("0 fichier json")  # pour investigation
        return "ETL.transforms_and_load_to_json.0_json_in_folder.A8_add_date_premiere_ecriture_attr"  # c'est le full_task_id (outer_group_id.inner_group_id.task_id)
    else:  # si 1 fichier json
        # print("1 fichier json")  # pour investigation
        return "ETL.transforms_and_load_to_json.1_json_in_folder.A7_special_jsons_concat"  # c'est le full_task_id (outer_group_id.inner_group_id.task_id)


@task(task_id="A7_special_jsons_concat")
def special_jsons_concatenation(aggregated_json_directory):
    """
    Fait la concaténation spéciale entre le json existant et le nouveau json comme telle que décrit dans :
    "api_extract__transform/outputs/offres/1--generated_json_file/troubleshooting/concatenation_dateExtraction_datePremiereEcriture/notes.xlsx".

    Retourne le nom du json qu'il reste dans le dossier, soit "new_json_file"
    """

    import pandas as pd

    now = datetime.now().strftime("%Y-%m-%d--%Hh%M")
    json_file_in_generated_directory = [file for file in os.listdir(aggregated_json_directory) if file.endswith(".json")]

    print(json_file_in_generated_directory)

    """
    Ici, on se retrouve normalement avec 2 fichiers jsons qu'on appellera par la suite :
      - "current_json_file" : pour le json déjà existant (toutes les offres récupérées aux itérations précédentes)
      - "new_json_file" : pour le json qui vient d'être créé (celui qui s'appelle "all_in_one.json")
    """

    #### current_json_file
    # Pour récupérer le nom de "current_json_file", on supprime "all_in_one.json" de la liste "json_file_in_generated_directory"
    json_file_in_generated_directory.remove("all_in_one.json")

    current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_1.json

    print(current_json_file)

    #### new_json_file : on renomme celui que la fonction "concatenate_all_json_into_one()" a créé (qui s'appellait "all_in_one.json")

    # A partir du json "curren_json_file", on construit le nom du json "new_json_file"
    # à supprimer : Création d'un nouveau json, créé à partir des nouvelles offres, avec de nouveaux appels API
    occurence_number = int(Path(current_json_file).stem.split("extraction_occurence_")[1])  # note : stem pour récupérer le nom du fichier sans l'extension
    new_json_file = f"{now}__extraction_occurence_{occurence_number+1}.json"

    os.rename(
        os.path.join(aggregated_json_directory, "all_in_one.json"),
        os.path.join(aggregated_json_directory, new_json_file),
    )

    # print(
    #     f'Il y a 1 fichier json dans le dossier "{generated_json_files_directory}"',
    #     f' -> json_1 = "{current_json_file}"',
    #     "",
    #     f"== Lancement de l'extraction occurence {occurence_number+1} ==",
    #     f'Création de json_2 = "{new_json_file}" à partir de nouvelles requêtes API, qui après traitement sera le seul json qui restera dans le dossier',
    #     sep="\n",
    # )
    print(
        f'Il y a 2 fichiers json dans le dossier "{aggregated_json_directory}"',
        f' -> json_1 = "{current_json_file}"',
        "",
        f' -> json_2 = "{new_json_file}"',  # , à partir de nouvelles requêtes API, qui après traitement sera le seul json qui restera dans le dossier',
        sep="\n",
    )

    print(f"\n==> Concaténation entre le json précédemment présent dans le dossier, et le json nouvellement créé\n")
    df1 = pd.read_json(os.path.join(aggregated_json_directory, current_json_file), dtype=False)
    df2 = pd.read_json(os.path.join(aggregated_json_directory, new_json_file), dtype=False)

    #
    intersection_ids = pd.merge(df1, df2, on="id")["id"].tolist()
    df1_minus_intersection = df1[~df1.id.isin(intersection_ids)]  # c'est la "partie_1" dans "workflow_db_update.drawio"
    df_concat = pd.concat([df1_minus_intersection, df2])  # concaténation de "partie_1" et "partie_2" (cf "workflow_db_update.drawio")

    # print("df1", df1.datePremiereEcriture.value_counts())  # pour investigation
    # print("df_concat", df_concat.datePremiereEcriture.value_counts())  # pour investigation

    # Pour faire ce qui est décrit ici "api_extract__transform/outputs/offres/1--generated_json_file/troubleshooting/...
    #   ...concatenation_dateExtraction_datePremiereEcriture/notes.xlsx" pour l'attribut "datePremiereEcriture".

    # df_concat.loc[df_concat["id"].isin(df1["id"]), "datePremiereEcriture"] = df1["datePremiereEcriture"]  # pb si les 2 df n'ont pas les mêmes index

    df_concat.set_index("id", inplace=True)
    df1.set_index("id", inplace=True)

    df_concat.loc[df1.index, "datePremiereEcriture"] = df1["datePremiereEcriture"]

    df_concat.reset_index(inplace=True)

    # print("df_concat après loc", df_concat.datePremiereEcriture.value_counts())  # pour investigation

    # print(
    #     "df1",
    #     df1[["id", "datePremiereEcriture", "dateExtraction"]],
    #     "df2",
    #     df2[["id", "dateExtraction"]],
    #     "df_concat",
    #     df_concat,
    #     sep="\n\n",
    # )  # pour investigation

    # Ecriture dans le fichier json
    df_concat.to_json(
        os.path.join(aggregated_json_directory, new_json_file),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs (on les supprimera à la fin du DAG)

    os.makedirs(os.path.join(aggregated_json_directory, "archives"), exist_ok=True)

    print('Déplacement de l\'ancien fichier json dans le dossier "archives"')

    source = os.path.join(aggregated_json_directory, current_json_file)
    destination = os.path.join(aggregated_json_directory, "archives", current_json_file)

    if os.path.exists(destination):
        os.remove(destination)  # supprime le fichier existant s'il existe déjà

    shutil.move(source, destination)

    print('Copie du nouveau fichier json dans le dossier "archives"')

    source = os.path.join(aggregated_json_directory, new_json_file)
    destination = os.path.join(aggregated_json_directory, "archives", new_json_file)

    shutil.copy(source, destination)

    return new_json_file


@task(task_id="A8_add_date_premiere_ecriture_attr")
def add_date_premiere_ecriture_attribute(aggregated_json_directory, json_filename, new_json_filename, date_to_insert=None, overwrite_all_lines=False):
    """
    Fonction qui charge le json et qui écrit dans un nouveau json : un nouvel attribut "datePremiereEcriture" avec la date désirée
      (par défaut la date système pour avoir la date du jour)

    Si le paramètre "overwrite_all_lines" est True, on écrase toutes les ligne de "datePremiereEcriture" avec la valeur de "date_to_insert".
      Sinon, seulement les lignes où "datePremiereEcriture" sont vides seront remplies avec "date_to_insert".

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """
    import numpy as np
    import pandas as pd

    print(f'\n==> Fonction "add_date_premiere_ecriture_attribute()"\n')

    if date_to_insert is None:
        date_to_insert = datetime.today().strftime("%Y-%m-%d")  # formatage en string 'YYYY-MM-DD'

    df = pd.read_json(os.path.join(aggregated_json_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

    # Créer la colonne "datePremiereEcriture" avec des NaN si elle n'existe pas
    if "datePremiereEcriture" not in df.columns:
        df["datePremiereEcriture"] = np.nan

    if overwrite_all_lines:
        # Si on veut écraser toutes les valeurs déjà écrites :
        df["datePremiereEcriture"] = pd.to_datetime(date_to_insert)  # sans la ligne suivante, on aura un timestamp en sortie de json "1743292800000"
        df["datePremiereEcriture"] = df["datePremiereEcriture"].dt.strftime("%Y-%m-%d")  # Formate les dates au format string 'YYYY-MM-DD'
    else:
        df["datePremiereEcriture"] = df["datePremiereEcriture"].fillna(date_to_insert)

    df.to_json(
        os.path.join(aggregated_json_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # print(df)  # pour investigation

    # On supprime les backslashs ajoutés par la méthode .to_json() [on le fait ici car c'est la dernière fonction]
    with open(os.path.join(aggregated_json_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace les "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(aggregated_json_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename


@task(task_id="A9_rename_json_file")
def rename_json_file(aggregated_json_directory, json_filename, new_json_filename):
    """Simple fonction qui renomme le fichier json"""
    print(f'Renommage du json "{os.path.join(aggregated_json_directory, json_filename)}" en "{os.path.join(aggregated_json_directory, new_json_filename)}"')
    os.rename(
        os.path.join(aggregated_json_directory, json_filename),
        os.path.join(aggregated_json_directory, new_json_filename),
    )


@task(task_id="A10_write_to_history", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
def write_to_history_csv_file(aggregated_json_directory):
    """
    Ecriture du nom du fichier et du nombre d'offres dans le fichier "_json_files_history.csv" pour historique
      avec le seul fichier json qu'il reste dans le dossier à ce stade

    Ne retourne rien.
    """

    import pandas as pd

    json_file_in_generated_directory = [file for file in os.listdir(aggregated_json_directory) if file.endswith(".json")]

    remaining_json_file = json_file_in_generated_directory[0]

    df = pd.read_json(
        os.path.join(aggregated_json_directory, remaining_json_file),
        dtype=False,  # pour ne pas inférer les dtypes
    )

    print(len(df))

    with open(os.path.join(aggregated_json_directory, "_json_files_history.csv"), "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([remaining_json_file, len(df)])

    return None


@task(task_id="A11_write_offers_ids_list_on_file_for_fastapi", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
def write_offers_ids_list_on_file_for_fastapi(aggregated_json_directory):
    """
    Extrait tous les "id" (tous les "offre_id" du json), et l'écrit dans un fichier, qui servira pour FastAPI.
    """

    import pandas as pd

    json_file_in_generated_directory = [file for file in os.listdir(aggregated_json_directory) if file.endswith(".json")]

    remaining_json_file = json_file_in_generated_directory[0]

    df = pd.read_json(
        os.path.join(aggregated_json_directory, remaining_json_file),
        dtype=False,  # pour ne pas inférer les dtypes
    )

    ids = df["id"]  # extraire la colonne 'id'

    logging.info(f'Nombre de "ids" à écrire : {len(df)}')

    cwd = os.getcwd()
    print(f"curdir : {cwd}")

    # enregistrer les identifiants dans un fichier texte
    ids.to_csv(
        os.path.join(CURRENT_DIR, "..", "fastapi", "offers_ids.txt"),  # dans le montage
        index=False,
        header=False,
        lineterminator="\n",
    )

    return None


# définition de paramètres liés au mécanisme de retry pour une tâche
default_args = {
    "retries": 5,  # nombre de tentatives de ré-exécution en cas d’échec d’une tâche
    "retry_delay": timedelta(minutes=1),  # délai entre deux tentatives de retry (après un échec)
    "retry_exponential_backoff": True,  # si True : le délai entre les retries augmente de façon exponentielle (ex: 2 min → 4 min → 8 min → ...)
    "max_retry_delay": timedelta(minutes=5),  # délai maximum entre deux retries, même si activation de backoff exponentiel
}


with DAG(
    dag_id="DAG_1_ETL",
    schedule="30 19 * * *",  # exécution tous les jours à 21h30 (attention il faut prendre en compte un offset de +2h dans la gui)
    catchup=False,  # pour ne pas rattraper les exécutions manquées
    tags=["project"],
    default_args=default_args,
):
    with TaskGroup(group_id="SETUP") as setup:
        with TaskGroup(group_id="check_files_in_folders") as check:
            check_csv_file_exists(LOCATION_CSV_FILENAME)  #### task S1
            check_appellations_yaml_file_exists(CODES_APPELLATION_FILENAME)  #### task S1
            check_credentials_yaml_file_exists(CREDENTIAL_FILENAME)  #### task S1

            delete_json = delete_all_in_one_json()  #### task S1
            count = count_number_of_json_file(AGGREGATED_JSON_DIR)  #### task S1

            delete_json >> count

        with TaskGroup(group_id="after_checks") as after_checks:
            remove_all_json_files(DOWNLOADED_JSONS_FROM_API_DIR)  #### task S2
            code_libelle_list = load_code_appellation_yaml_file()  #### task S2
            dict_ = get_creds_from_yaml_file(CREDENTIAL_FILENAME)  #### task S2
            token = get_bearer_token(dict_, SCOPES_OFFRES)  #### task S2

        check >> after_checks

    with TaskGroup(group_id="ETL") as etl:
        api_requests = get_offers.partial(token=token).expand(code_libelle_list=code_libelle_list)  #### task A1
        # notes : 1/ "partial()" car token commun à toutes les tâches mappées, 2/ "expand()" car 1 task par valeur de la liste "code_libelle_list"

        with TaskGroup(group_id="transforms_and_load_to_json") as tl:
            all_json_in_one = concatenate_all_json_into_one(DOWNLOADED_JSONS_FROM_API_DIR, AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME)  #### task A2

            # note : pour les fonctions suivantes, on prend le fichier "all_in_one_json" et on écrase son contenu.
            metropole = keep_only_offres_from_metropole(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME)  #### task A3
            add_location = add_location_attributes(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME)  #### task A4
            add_date_extract = add_date_extract_attribute(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME, None)  #### task A5
            # notes : 1/ "None" pour avoir la date du jour, 2/ date_to_insert="2025-03-02"  pour écraser la valeur si l'attribut est existant dans le json

            branch = nb_json_on_setup_0_or_1(count)  #### task A6

            all_json_in_one >> metropole >> add_location >> add_date_extract >> branch

            with TaskGroup(group_id="0_json_in_folder") as file0:
                now = datetime.now().strftime("%Y-%m-%d--%Hh%M")
                new_json_filename = f"{now}__extraction_occurence_1.json"

                add_date_first_0 = add_date_premiere_ecriture_attribute(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME, None, False)  #### task A8
                json_rename = rename_json_file(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, new_json_filename)  #### task A9

                add_date_first_0 >> json_rename

            with TaskGroup(group_id="1_json_in_folder") as file1:
                json_concat_filename = special_jsons_concatenation(AGGREGATED_JSON_DIR)  #### task A7
                add_date_first_1 = add_date_premiere_ecriture_attribute(AGGREGATED_JSON_DIR, json_concat_filename, json_concat_filename, None, False)  #### task A8

                json_concat_filename >> add_date_first_1

            branch >> file0
            branch >> file1

        write_history = write_to_history_csv_file(AGGREGATED_JSON_DIR)  #### task A10
        write_offers_ids = write_offers_ids_list_on_file_for_fastapi(AGGREGATED_JSON_DIR)  #### task A11

        api_requests >> tl
        [file0, file1] >> write_history
        [file0, file1] >> write_offers_ids

    trigger_dag2 = TriggerDagRunOperator(  #### task finale qui déclenche le DAG 2 si DAG 1 en "success"
        task_id="trigger_dag_2",
        trigger_dag_id="DAG_2_WRITE_TO_DATABASE",
        wait_for_completion=False,
        reset_dag_run=True,
    )

    write_history >> trigger_dag2

    setup >> etl
