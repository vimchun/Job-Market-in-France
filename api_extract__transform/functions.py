import json
import os

import pandas as pd
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

    return None


def get_offres(token, code_appellation_libelle, filter_params):
    """
    A partir des appellations ROME décrites dans "code_appellation_libelle.yml", récupérer les offres de chaque appellation et les écrit dans un fichier json.
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150.

    Ne retourne rien.
    """

    appellation = filter_params["appellation"]

    # libelle = ""

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
            # output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}_{libelle}__{max_offres}_offres.json")
            output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}_{libelle}.json")
        else:
            # output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}__{max_offres}_offres.json")
            output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}.json")

        if os.path.exists(output_file):
            os.remove(output_file)

    ###### réponse 200 : on peut déjà récupérer toutes les offres disponibles
    if response.status_code == 200:
        print(f"Status Code: {response.status_code}")
        # print(response.headers.get("Content-Range"))
        print(f"  => {Fore.CYAN}[{max_offres}]{Style.RESET_ALL} offres au total {Fore.YELLOW}--> écriture dans le fichier")

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

        # Renommer les fichiers json en ajoutant le nombre d'offres dans le json
        dir_path, file_name = os.path.split(output_file)  # Séparer le chemin et le nom du fichier
        new_file_name = f"{file_name[:-5]}__{document_id}_offres.json"
        # print(dir_path, file_name, new_file_name, sep="\n")  # utile si investigation
        new_file_path = os.path.join(dir_path, new_file_name)  # Créer le chemin complet du nouveau fichier
        os.rename(output_file, new_file_path)  # Renommer le fichier

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
                        f.write(",\n")  # Ajouter une virgule après chaque objet
                        document_id += 1
                    print(f"{range_start}-{range_end}/{max_offres} {Fore.YELLOW}--> écriture dans le fichier (total: {document_id})")
                else:
                    print(f"Status Code: {response.status_code}, {response.json()}")
                    break

                range_start += 150
                range_end += 150
                filter_params["range"] = f"{range_start}-{range_end}"
                request_id += 1

                # if request_id == 2:  # utile si besoin investigation
                #     break

        """
        A partir d'ici, on applique le principe du script "fix_invalid_json.py" :
            - On a un json invalide jusqu'ici, de la forme suivante (simplifiée ici) :

                ```
                [
                {"id": "188VMGQ", "intitule": "Data Engineer (H/F)"},
                {"id": "188RQRZ", "intitule": "Responsable Data Studio F/H (H/F)"},
                {"id": "188PNVQ", "intitule": "Maître du Jeu des ETL recherché pour notre Next Game"},
                    // ligne vide
                ```

            - Et on va rendre ce json valide, et ainsi avoir

                ```
                [
                {"id": "188VMGQ", "intitule": "Data Engineer (H/F)"},
                {"id": "188RQRZ", "intitule": "Responsable Data Studio F/H (H/F)"},
                {"id": "188PNVQ", "intitule": "Maître du Jeu des ETL recherché pour notre Next Game"}
                ]
                ```

        """
        # Ecrire le contenu de "invalid_json.json" dans "invalid_content"
        with open(output_file, "r") as invalid:
            invalid_content = invalid.read()
            # print(invalid_content)

        # Ecrire le json valide dans "valid_content"
        with open(output_file, "w") as valid:
            valid_content = invalid_content[:-2] + "\n]"
            valid.write(valid_content)

        # Ouvrir le fichier json valide pour vérifier qu'il est bien valide
        with open(output_file, "r") as valid:
            valid_content = valid.read()
            try:
                json.loads(valid_content)
                print("Le json est bien valide.")
            except json.JSONDecodeError as e:
                print(f"Le json n'est pas valide :\n==> {e}")

        # Renommer les fichiers json en ajoutant le nombre d'offres dans le json
        dir_path, file_name = os.path.split(output_file)  # Séparer le chemin et le nom du fichier
        new_file_name = f"{file_name[:-5]}__{document_id}_offres.json"
        # print(dir_path, file_name, new_file_name, sep="\n")  # utile si investigation
        new_file_path = os.path.join(dir_path, new_file_name)  # Créer le chemin complet du nouveau fichier
        os.rename(output_file, new_file_path)  # Renommer le fichier

    ###### autres cas
    elif response.status_code == 204:
        print(f"Status Code : {response.status_code} : Aucune offre correspondante")
    else:
        print(f"Status Code : {response.status_code} ==> {response.json()}")

    print("")

    return None


def concatenate_all_json_into_one(json_files_directory, concat_json_filename):
    """
    Nous obtenons suite à l'exécution de get_offres() x fichiers json (x = nombre d'appellations présents dans "code_appellation_libelle.yml").
    Cette fonction écrira dans un json chaque ligne de tous les json précédents, en supprimant les doublons.

    Renvoie le DateFrame qui concatène toutes les offres, sans doublon.
    """

    df_concat = pd.DataFrame()

    for filename in os.listdir(json_files_directory):
        if filename.endswith(".json") and filename != concat_json_filename:  # traite aussi le cas du fichier sans extension
            print(filename)
            try:
                # si le json est bien valide
                with open(os.path.join(json_files_directory, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                df_concat = pd.concat([df, df_concat], ignore_index=True)

            except json.JSONDecodeError as e:
                print(f"{Fore.RED}Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
            except FileNotFoundError:
                print(f'{Fore.RED}Le fichier "{filename}" n\'a pas été trouvé.')
            except Exception as e:
                print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")

    print(f"\n --> df_concat : {df_concat.shape[0]} offres, df_concat_drop_duplicates : {df_concat.drop_duplicates(["id"]).shape[0]} offres")

    df_concat.drop_duplicates(["id"]).to_json(
        os.path.join(json_files_directory, concat_json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, concat_json_filename), "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("\\/", "/")

    # On sauvegarde le fichier final sans les '\'
    with open(os.path.join(json_files_directory, concat_json_filename), "w", encoding="utf-8") as f:
        f.write(content)

    return df_concat.drop_duplicates(["id"])
