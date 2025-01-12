import json
import os

import requests

from colorama import Fore, Style, init

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


token = ""
current_directory = os.path.dirname(os.path.abspath(__file__))


def get_bearer_token(client_id, client_secret, scope):
    """
    Récupère un Bearer Token grâce à l'API de France Travail.

    Paramètres :
    - client_id (str) : Identifiant client fourni par l'API de France Travail.
    - client_secret (str) : Clé secrète fournie par l'API de France Travail.
    - scope (str) : Liste des scopes séparés par des espaces, indiquant les permissions demandées.

    Return :
    - str : Le Bearer Token pour l'authentification des requêtes, ou None en cas d'erreur.
    """
    print(f"{Fore.GREEN}== Récupération du bearer token :")

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


def get_referentiel_appellations_rome(token):
    """
    https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/api-reference/operations/recupererReferentielAppellations
    Récupérer le référentiel des appellations ROME et les écrit dans un fichier json.
    Ne retourne rien.
    Un "code" correspond à un "libelle", par exemple { "code": "404278", "libelle": "Data engineer" }
    """
    print(f"{Fore.GREEN}== Récupération du référentiel des appellations ROME:")

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
            json.dump(data, f, ensure_ascii=False, indent=4)

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
    print(f"{Fore.GREEN}== Récupération du référentiel des pays :")

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
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

    return None


def get_offres(token, code_appellation_libelle, filter_params):
    """
    A partir des appellations ROME décrites dans "code_appellation_libelle.yml", récupérer les offres de chaque appellation et les écrit dans un fichier json.
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150.

    Ne retourne rien.
    """
    appellation = filter_params["appellation"]

    libelle = ""

    for item in code_appellation_libelle:
        if item["code"] == appellation:
            libelle = item["libelle"]
            break

    codes_list = [str(i["code"]) for i in code_appellation_libelle]

    if filter_params["appellation"] in codes_list:
        print(f"{Fore.GREEN}== Récupération des offres ({appellation}: {libelle}) :")
    else:
        print(f"{Fore.GREEN}== Récupération des offres ({appellation}) :")

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    #### Première requête pour voir combien d'offres sont disponibles

    response = requests.get(url, headers=headers, params=filter_params)

    print(f"{Fore.GREEN}==== Récupération des offres (requête 0), pour connaître le nombre d'offres :", end=" ")

    # print(
    #     response,
    #     response.headers.get("Content-Range"),  # exemple : "offres 0-0/9848"
    #     int(response.headers.get("Content-Range").split("/")[-1]),
    # )

    max_offres = 0
    output_file = ""

    if response.status_code in [200, 206]:
        content_range = response.headers.get("Content-Range")
        if content_range is not None:
            max_offres = int(content_range.split("/")[-1])

        if filter_params["appellation"] in codes_list:
            output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}_{libelle}__{max_offres}_offres.json")
        else:
            output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}__{max_offres}_offres.json")

        if os.path.exists(output_file):
            os.remove(output_file)

    ###### réponse 200 : on peut récupérer déjà récupérer toutes les offres disponibles
    if response.status_code == 200:
        print(f"Status Code: {response.status_code}")
        # print(response.headers.get("Content-Range"))
        print(f"  => {Fore.CYAN}[{max_offres}]{Style.RESET_ALL} offres au total {Fore.YELLOW}--> writing to file")

        document_id = 0

        with open(output_file, "a", encoding="utf-8") as f:
            f.write("[\n")  # Ajouter un "[" pour "initialiser" le fichier json

            for obj in response.json()["resultats"]:  # Boucle for pour écrire uniquement les documents
                json.dump(obj, f, ensure_ascii=False)
                if document_id < max_offres - 1:
                    f.write(",\n")  # Ajouter une virgule après chaque objet
                else:
                    f.write("\n")  # Pour le dernier document, on ne met pas de virgule, sinon le json n'est pas valide
                document_id += 1

            f.write("]")  # Clore le json en ajoutant un crochet fermant "]"

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
        filter_params["range"] = f"{range_start}-{range_end}"

        with open(output_file, "a", encoding="utf-8") as f:
            f.write("[\n")  # Ajouter un "[" pour "initialiser" le fichier json

            document_id = 0

            for _ in range(int(max_offres / 150) + 1):
                print(f"{Fore.GREEN}==== Récupération des offres (requête {request_id}) :", end=" ")
                response = requests.get(url, headers=headers, params=filter_params)

                if response.status_code == 206:
                    print(f"Status Code: {response.status_code}", end=", ")

                    # Boucle for pour écrire uniquement les documents
                    for obj in response.json()["resultats"]:
                        json.dump(obj, f, ensure_ascii=False)
                        # Si on écrit le dernier document possible (le 3150e), on ne met pas de virgule à la fin, sinon le json n'est pas valide
                        if document_id == 3149:
                            f.write("\n")  # Pour le dernier document, on ne met pas de virgule, sinon le json n'est pas valide
                        else:
                            if document_id < max_offres - 1:
                                f.write(",\n")  # Ajouter une virgule après chaque objet
                            else:
                                f.write("\n")  # Pour le dernier document, on ne met pas de virgule, sinon le json n'est pas valide
                        document_id += 1
                    print(f"{range_start}-{range_end}/{max_offres} {Fore.YELLOW}--> writing to file")
                else:
                    print(f"Status Code: {response.status_code}, {response.json()}")
                    break

                range_start += 150
                range_end += 150
                filter_params["range"] = f"{range_start}-{range_end}"
                request_id += 1

            f.write("]")  # Clore le json en ajoutant un crochet fermant "]"

    ###### autres cas
    elif response.status_code == 204:
        print(f"Status Code : {response.status_code} : Aucune offre correspondante")
    else:
        print(f"Status Code : {response.status_code} ==> {response.json()}")

    print("")

    return None


def merge_all_json_into_one(json_files_directory, merged_json_filename):
    """
    Nous obtenons suite à l'exécution de get_offres() x fichiers json (x = nombre d'appellations présents dans "code_appellation_libelle.yml").
    Cette fonction écrira dans un json chaque ligne de tous les json précédents, en supprimant les doublons.
    """

    import pandas as pd

    df_merged = pd.DataFrame()

    for filename in os.listdir(json_files_directory):
        if filename.endswith(".json") and filename != merged_json_filename:  # traite aussi le cas du fichier sans extension
            print(filename)
            try:
                # si le json est bien valide
                with open(os.path.join(json_files_directory, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df_merged = pd.concat([df, df_merged], ignore_index=True)

            except json.JSONDecodeError as e:
                print(f"{Fore.RED}Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
            except FileNotFoundError:
                print(f'{Fore.RED}Le fichier "{filename}" n\'a pas été trouvé.')
            except Exception as e:
                print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")

    print(f"\n --> df_merged : {df_merged.shape[0]} offres, df_merged_drop_duplicates : {df_merged.drop_duplicates(["id"]).shape[0]} offres")

    df_merged.drop_duplicates(["id"]).to_json(os.path.join(json_files_directory, merged_json_filename))

    return None


def merged_json_file_to_pd_dataframe(merged_json_filename_path):
    """
    Prend simplement le fichier json fusionné et retourne le Dataframe Pandas associé
    """
    import pandas as pd

    with open(merged_json_filename_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return pd.DataFrame(data)
