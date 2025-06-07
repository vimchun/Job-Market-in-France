import json
import os
import time

from datetime import datetime

import numpy as np
import pandas as pd
import requests
import unidecode

from colorama import Fore, Style, init
from geopy.geocoders import Nominatim

from airflow.decorators import task

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

current_directory = os.path.dirname(os.path.abspath(__file__))


#### fonctions utilisées par airflow (décorateur @task)


@task(task_id="S1_check_nb_of_json_files")
def count_json_files_number(directory_path):
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
        print(f"==> Au moins 2 fichiers json ({count} fichiers : {json_files}). On arrête le DAG.")
        # raise Exception(f"==> Au moins 2 fichiers json ({count} fichiers : {json_files}). On arrête le DAG.") # todo: à remettre une fois le dev avancé

    return json_files


@task(task_id="S2_check_yaml_file_presence")
def check_presence_yaml_file(file_path):
    """
    Vérifie la présence du fichier yaml "file_path".
      - Si True, on continue le DAG.
      - Sinon, on arrête le DAG avec une Exception.
    """
    if os.path.exists(file_path):
        print(f'Le fichier yaml est bien présent ici : "{file_path}", on continue le DAG...')
    else:
        raise Exception(f"==> Le fichier yaml n'est pas présent dans ({file_path}). On arrête le DAG.")

    return None


@task(task_id="S3_remove_all_json_files")
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


@task(task_id="S4_get_token")
def get_bearer_token(client_id, client_secret, scope):
    """
    Récupère un Bearer Token grâce à l'API de France Travail.

    Paramètres :
    - client_id (str) : Identifiant client fourni par l'API de France Travail.
    - client_secret (str) : Clé secrète fournie par l'API de France Travail.
    - scope (str) : Liste des scopes séparés par des espaces, indiquant les permissions demandées.

    Retourne :
    - Bearer Token (str) : pour l'authentification des requêtes, ou None en cas d'erreur.
    """

    print(f'{Fore.GREEN}\n==> Fonction "get_bearer_token()"\n')

    # paramètres décrits ici https://francetravail.io/produits-partages/documentation/utilisation-api-france-travail/generer-access-token
    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    params = {"realm": "/partenaire"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
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


@task(task_id="S5_load_yaml_file")
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

    codes_appellation_filename = os.path.join(current_directory, "..", "..", "data", "resources", "code_appellation_libelle.yml")

    with open(codes_appellation_filename, "r") as file:
        content = yaml.safe_load(file)
        code_libelle_list = content["code_appellation_libelle"]

    return code_libelle_list


@task(task_id="S6_create_name_for_concat_json_file")
def create_name_for_concat_json_file():
    """
    Retourne le nom du futur fichier json qui concatènera toutes les offres,
      construit à partir de la dernière écriture dans le fichier "_json_files_history.csv"
    """
    import csv

    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_directory, "..", "..", "data", "outputs", "offres", "1--generated_json_file", "_json_files_history.csv")

    with open(csv_file, "r") as f:
        reader = list(csv.DictReader(f))

    last_occurence = int(reader[-1]["json_filename"].split("occurence_")[1].split(".json")[0])

    now = datetime.now().strftime("%Y-%m-%d--%Hh%M")

    filename = f"{now}__extraction_occurence_{last_occurence+1}.json"

    return filename


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


# @task(pool="api_francetravail_pool", retries=3, retry_delay=timedelta(seconds=10))
@task(task_id="A1_get_offers")
def get_offers(token, code_libelle_list):
    """
    Récupére les offres de chaque appellation et les écrit dans un fichier json à partir des appellations ROME décrites dans "code_appellation_libelle.yml"
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150.
    A noter qu'on a droit à 10 maximum par seconde (sinon erreur 429 ("too much requests")).

    Ne retourne rien.
    """

    # todo : créer un pool pour gérer le nombre de tâches en // ?

    code_appellation = code_libelle_list["code"]
    libelle = code_libelle_list["libelle"]

    output_file_path = os.path.join(current_directory, "..", "..", "data", "outputs", "offres", "0--original_json_files_from_api")
    output_file = os.path.join(output_file_path, f"{code_appellation}_{libelle}.json")

    if os.path.exists(output_file):
        os.remove(output_file)

    offers_data = []

    print(f"{Fore.GREEN}== Récupération des offres ({code_appellation}: {libelle}) :")

    #### Première requête pour voir combien d'offres sont disponibles

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    params = {"appellation": code_appellation, "paysContinent": "01"}

    response = throttled_get(url, headers=headers, params=params, max_retries=10, retry_delay=2)

    print(f"{Fore.GREEN}==== Récupération des offres (requête 0), pour connaître le nombre d'offres :", end=" ")

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
        print(f"  => {Fore.CYAN}[{max_offres}]{Style.RESET_ALL} offres au total {Fore.YELLOW}--> écriture dans le fichier")

        document_id = 0

        for obj in response.json()["resultats"]:
            offers_data.append(obj)
            document_id += 1

    ###### réponse 206 : on doit faire plusieurs requêtes pour récupérer tous les documents (limité à 3150 documents)
    elif response.status_code == 206:
        print(f"Status Code: {response.status_code} (Réponse partielle)")
        # print(response.headers.get("Content-Range"))
        print(f"  => {Fore.CYAN}[{max_offres}]{Style.RESET_ALL} offres au total")
        print(f"  => {Fore.CYAN}[{int(max_offres/150)+1}]{Style.RESET_ALL} requêtes nécessaires (avec 150 documents) pour tout récupérer", end="")
        print(f" {Style.DIM} (limité à 21 requêtes, soit 3150 offres maximum)")  # (voir limitation du paramètre range)

        range_start = 0
        range_end = 149
        request_id = 1
        params["range"] = f"{range_start}-{range_end}"

        document_id = 0

        for _ in range(int(max_offres / 150) + 1):
            print(f"{Fore.GREEN}==== Récupération des offres (requête {request_id}) :", end=" ")
            response = throttled_get(url, headers=headers, params=params, max_retries=10, retry_delay=2)

            if response.status_code == 206:
                print(f"Status Code: {response.status_code}", end=", ")

                for obj in response.json()["resultats"]:
                    offers_data.append(obj)
                    document_id += 1
                print(f"{range_start}-{range_end}/{max_offres} {Fore.YELLOW}--> écriture dans le fichier (total: {document_id})")

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
def concatenate_all_json_into_one(json_files_from_api_directory, generated_json_file_directory, new_json_filename):
    """
    On obtient suite à l'exécution de `get_offres()` x fichiers json (x = nombre d'appellations présents dans "code_appellation_libelle.yml").
    Cette présente fonction écrit dans un nouveau json tous les documents json de chaque fichier présent dans le dossier "json_files_from_api_directory", en supprimant les doublons.

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """

    print(f'{Fore.GREEN}\n==> Fonction "concatenate_all_into_one()"\n')

    df_concat = pd.DataFrame()

    for filename in os.listdir(json_files_from_api_directory):
        if filename.endswith(".json"):  # and filename != concat_json_filename:  # traite aussi le cas du fichier sans extension
            print(filename)
            try:
                # si le json est bien valide
                with open(os.path.join(json_files_from_api_directory, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df_concat = pd.concat([df_concat, df], ignore_index=True)

            except json.JSONDecodeError as e:
                print(f"{Fore.RED}Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
            except FileNotFoundError:
                print(f'{Fore.RED}Le fichier "{filename}" n\'a pas été trouvé.')
            except Exception as e:
                print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")

    num_offres_without_duplicates = len(df_concat.drop_duplicates(["id"]))
    print(f"\n --> df_concat : {df_concat.shape[0]} offres, df_concat_drop_duplicates : {num_offres_without_duplicates} offres\n\n")

    df_concat.drop_duplicates(["id"]).to_json(
        os.path.join(generated_json_file_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # print(df_concat)  # pour investigation

    # todo: répétés plusieurs fois dans les fonctions suivantes donc à factoriser (ou ne le faire qu'à la fin ?)
    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(generated_json_file_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(generated_json_file_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename


@task(task_id="A3_only_metropole")
def keep_only_offres_from_metropole(json_files_directory, json_filename, new_json_filename):
    """
    Cette fonction écrase le json entré en paramètre, en ne conservant que les offres d'emploi de la France Métropolitaine.
    Elle ne conserve pas les offres de la Corse ni des DOMTOM.

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
     et aussi le nombre de ligne du DataFrame (si on en a besoin pour renommer le fichier, mais on ne le fera pas conformément au workflow)
    """

    print(f'{Fore.GREEN}\n==> Fonction "keep_only_offres_from_metropole()"\n')

    df = pd.read_json(
        os.path.join(json_files_directory, json_filename),
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
        os.path.join(json_files_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace les "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(json_files_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename, len(df_only_metropole)


@task(task_id="A4_add_location_attrs")
def add_location_attributes(json_files_directory, json_filename, new_json_filename):
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

    print(f'{Fore.GREEN}\n==> Fonction "add_location_attributes()"\n')

    # Chargement des fichiers
    # =======================
    current_directory = os.path.dirname(os.path.abspath(__file__))

    print(f"\n====> Chargement des fichiers\n")

    df = pd.read_json(
        os.path.join(json_files_directory, json_filename),
        dtype=False,  # désactiver l'inférence des types
    )

    df_insee = pd.read_csv(
        os.path.join(os.path.join(current_directory, "..", "..", "data", "resources", "code_name__city_department_region.csv")),
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
    # =================================
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
    # =================================================================================================

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
    # ================================================================================================================================

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
    # ===============================================================================================

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
    # =======================================================================================================================

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
    # ====================================

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
    df_lieu = df_lieu.drop(
        ["intitule", "libelle", "latitude", "longitude"],
        axis=1,
    )

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
    df = df.drop(
        ["lieuTravail", "libelle", "latitude", "longitude", "codePostal", "commune"],
        axis=1,
    )

    df_final = pd.merge(left=df, right=df_lieu, on="id")

    # Ecriture dans un fichier .json
    # ==============================

    df_final.to_json(
        os.path.join(json_files_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(json_files_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename


@task(task_id="A5_add_date_extract")
def add_date_extract_attribute(json_files_directory, json_filename, new_json_filename, date_to_insert=None):
    """
    Fonction qui charge le json et qui écrit dans un nouveau json : un nouvel attribut "date_extraction" avec la date désirée
      (par défaut la date système pour avoir la date du jour)

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """

    print(f'{Fore.GREEN}\n==> Fonction "add_date_extract_attribute()"\n')

    if date_to_insert is None:
        # date_to_insert = datetime.today().date()  # .date() pour ne pas avoir l'heure
        date_to_insert = datetime.today().strftime("%Y-%m-%d")  # formatage en string 'YYYY-MM-DD'

    df = pd.read_json(
        os.path.join(json_files_directory, json_filename),
        dtype=False,  # pour ne pas inférer les dtypes
    )

    df["dateExtraction"] = pd.to_datetime(date_to_insert)  # sans la ligne suivante, on aura un timestamp en sortie de json "1743292800000"
    df["dateExtraction"] = df["dateExtraction"].dt.strftime("%Y-%m-%d")  # Formate les dates au format string 'YYYY-MM-DD'

    df.to_json(
        os.path.join(json_files_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # print(df)  # pour investigation

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace les "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(json_files_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename


def add_date_premiere_ecriture_attribute(json_files_directory, json_filename, new_json_filename, date_to_insert=None, overwrite_all_lines=False):
    """
    Fonction qui charge le json et qui écrit dans un nouveau json : un nouvel attribut "datePremiereEcriture" avec la date désirée
      (par défaut la date système pour avoir la date du jour)

    Si le paramètre "overwrite_all_lines" est vrai, on écrase toutes les ligne de "datePremiereEcriture" avec "date_to_insert".
      Sinon, seulement les lignes où "datePremiereEcriture" sont vides seront remplies avec "date_to_insert".

    Renvoie le nom du json généré qui conformément au workflow devrait être le nom du fichier en entrée puisqu'on l'écrase (paramétrable au cas où)
    """

    print(f'{Fore.GREEN}\n==> Fonction "add_date_premiere_ecriture_attribute()"\n')

    if date_to_insert is None:
        date_to_insert = datetime.today().strftime("%Y-%m-%d")  # formatage en string 'YYYY-MM-DD'

    df = pd.read_json(os.path.join(json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

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
        os.path.join(json_files_directory, new_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # print(df)  # pour investigation

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, new_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace les "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(json_files_directory, new_json_filename), "w", encoding="utf-8") as f:
            f.write(content)

    return new_json_filename


#### fonctions non utilisées par airflow (pas de décorateur @task), pas vraiment utile au projet mais peuvent servir


def get_referentiel_appellations_rome(token):
    """
    https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/api-reference/operations/recupererReferentielAppellations
    Récupérer le référentiel des appellations ROME et les écrit dans un fichier json.
    Ne retourne rien.
    Un "code" correspond à un "libelle", par exemple { "code": "404278", "libelle": "Data engineer" }
    """
    print(f'{Fore.GREEN}\n==> Fonction "get_referentiel_appellations_rome()" :\n')

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Status Code: {response.status_code}\n")
        # print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
        # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)

        file_path = os.path.join(current_directory, "outputs", "referentiels", "appellations_rome.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            #     json.dump(data, f, ensure_ascii=False, indent=4)  # écrit le json, mais le formattage classique prend trop de place... le code suivant corrige le tir # noqa
            f.write("[\n")  # Ajouter un "[" pour "initialiser" le fichier json
            for i in range(len(data)):
                f.write("    ")
                json.dump(data[i], f, ensure_ascii=False)
                if i < len(data) - 1:  # Ajouter une virgule pour tous les documents sauf pour le dernier
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]")  # Clore le json en ajoutant un crochet fermant "]"

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

    return None


def get_referentiel_pays(token):
    """
    https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/api-reference/operations/recupererReferentielPays
    Récupérer le référentiel des pays et les écrit dans un fichier json.
    Ne retourne rien.
    Un "code" correspond à un "libelle", par exemple  { "code": "01", "libelle": "France" }
    """
    print(f'{Fore.GREEN}\n==> Fonction "get_referentiel_pays()"\n')

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/pays"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Status Code: {response.status_code}\n")
        # print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
        # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)

        file_path = os.path.join(current_directory, "outputs", "referentiels", "pays.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            # json.dump(data, f, ensure_ascii=False, indent=4) # écrit le json, mais le formattage classique prend trop de place... le code suivant corrige le tir # noqa
            f.write("[\n")  # Ajouter un "[" pour "initialiser" le fichier json
            for i in range(len(data)):
                f.write("    ")
                json.dump(data[i], f, ensure_ascii=False)
                if i < len(data) - 1:  # Ajouter une virgule pour tous les documents sauf pour le dernier
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]")  # Clore le json en ajoutant un crochet fermant "]"

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

    return None


def create_csv__code_name__city_department_region():
    """
    Créé à partir du notebook "1--create_csv_codes__city_departement_region.ipynb".
    Génère le fichier "Job_Market/api_extract__transform/locations_information/code_name__city_department_region" qui sert à récupérer les informations suivantes :

        - code_insee
        - nom_commune
        - code_postal
        - nom_ville
        - code_departement
        - nom_departement
        - code_region
        - nom_region

    Ne retourne rien.
    """

    print(f'{Fore.GREEN}\n==> Fonction "create_csv__code_name__city_department_region()"\n')

    # todo : ajouter la partie download / unzip des fichiers (pas urgent)

    # Fichiers du lien_2
    # ==================

    current_directory = os.path.dirname(os.path.abspath(__file__))

    files_directory = os.path.join(
        current_directory,
        "locations_information",
        "archives",
    )
    file_commune = "v_commune_2024.csv"
    file_departement = "v_departement_2024.csv"
    file_region = "v_region_2024.csv"

    # df_commune
    # ==========

    df_commune = pd.read_csv(
        os.path.join(files_directory, "lien_2", file_commune),
        usecols=["COM", "REG", "DEP", "LIBELLE"],
    )

    df_commune.rename(
        {
            "COM": "code_insee",
            "REG": "code_region",
            "DEP": "code_departement",
            "LIBELLE": "nom_commune",
        },
        axis=1,
        inplace=True,
    )

    # On ajoute une colonne nom_ville (idem que nom_commune sans les arrondissements pour Paris, Marseille et Lyon)
    #  car on va préférer "Lyon" à "Lyon 1er Arrondissement" ou "Lyon 2e Arrondissement"...

    df_commune["nom_ville"] = df_commune.apply(
        lambda x: x.nom_commune.split(" ")[0] if "Arrondissement" in x.nom_commune else x.nom_commune,
        axis=1,
    )

    df_departement = pd.read_csv(
        os.path.join(files_directory, "lien_2", file_departement),
        usecols=["DEP", "LIBELLE"],
    )

    df_departement.rename(
        {"DEP": "code_departement", "LIBELLE": "nom_departement"},
        axis=1,
        inplace=True,
    )

    df_region = pd.read_csv(
        os.path.join(files_directory, "lien_2", file_region),
        usecols=["REG", "LIBELLE"],
    )

    df_region.rename(
        {"REG": "code_region", "LIBELLE": "nom_region"},
        axis=1,
        inplace=True,
    )

    # On exclut les régions hors de la France Métropolitaine
    df_region = df_region[~df_region.nom_region.isin(["Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte", "Corse"])]

    # merging

    df_lien_2 = df_commune.merge(df_departement, on="code_departement").merge(df_region, on="code_region")

    # pour avoir code_region = 84 au lieu de 84.0 par exemple
    df_lien_2.code_region = df_lien_2.code_region.astype(int).astype(str)

    df_lien_2 = df_lien_2[
        [
            "code_insee",
            "nom_commune",
            "nom_ville",
            "code_departement",
            "nom_departement",
            "code_region",
            "nom_region",
        ]
    ]

    # Fichier du lien_3
    # =================

    # Mapping code insee <> code postal

    df_lien_3 = pd.read_csv(
        os.path.join(files_directory, "lien_3", "cities.csv"),
        usecols=["insee_code", "zip_code"],
    )

    df_lien_3.rename(
        {"insee_code": "code_insee", "zip_code": "code_postal"},
        axis=1,
        inplace=True,
    )

    df_lien_3[df_lien_3.code_insee == "75056"]  # non disponible dans ce fichier, donc attention au merge

    df_lien_3["code_postal"] = df_lien_3["code_postal"].astype(str)

    # Merge des df des liens 2 et 3
    # =============================

    df = pd.merge(left=df_lien_2, right=df_lien_3, on="code_insee", how="left")
    # left car tous les code_insee ne sont pas disponibles dans df_lien_3

    df = df[
        [
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

    df["code_postal"] = df["code_postal"].str.zfill(5)

    df = df.drop_duplicates(["code_insee", "code_postal"])

    # Ecriture dans un fichier .csv
    # =============================

    df.to_csv(
        os.path.join(
            current_directory,
            "locations_information",
            "code_name__city_department_region.csv",
        ),
        index=False,  # pour ne pas écrire les index
    )
