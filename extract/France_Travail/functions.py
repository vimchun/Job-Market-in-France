import json
import os
import sys

import requests

from colorama import Back, Fore, Style, init

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


def get_appellations(token):
    """
    Récupérer les appellations et les écrit dans un fichier json.
    Ne retourne rien.
    Un "code" correspond à un "libelle", par exemple :

     - { "code": "404278", "libelle": "Data engineer" }
    """
    print(f"{Fore.GREEN}== Récupération des appellations :")

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

        file_path = os.path.join(current_directory, "outputs", "appellations.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

    return None


def get_offres(token, filter_params):
    """
    Récupérer les offre et les écrit dans un fichier json.
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150

    Ne retourne rien.
    """
    # print(f"{Fore.GREEN}== Récupération des offres :")

    # current_directory = os.path.dirname(os.path.abspath(__file__))

    appellation = filter_params["appellation"]

    # Recherche le "libelle" correspondant à "l'appellation"

    code_libelle = [
        {"code": "38970", "libelle": "Data_Miner"},
        {"code": "38971", "libelle": "Data_Analyst"},
        {"code": "38972", "libelle": "Data_Scientist"},
        {"code": "38975", "libelle": "Data_Manager"},
        {"code": "38977", "libelle": "Developpeur_Big_Data"},
        {"code": "404274", "libelle": "Ingenieur_Data_Scientist"},
        {"code": "404276", "libelle": "Architecte_Big_Data"},
        {"code": "404277", "libelle": "Big_Data_Engineer"},
        {"code": "404278", "libelle": "Data_Engineer"},
        {"code": "404279", "libelle": "Docteur_Big_Data"},
        {"code": "404280", "libelle": "Expert_Big_Data"},
        {"code": "404281", "libelle": "Expert_Technique_Big_Data"},
        {"code": "404282", "libelle": "Ingenieur_Dig_Data"},
        {"code": "404283", "libelle": "Ingenieur_Dataviz"},
        {"code": "404285", "libelle": "Ingenieur_En_Developpement_Big_Data"},
        {"code": "404286", "libelle": "Responsable_Architecture_Conception_Data"},
        {"code": "404287", "libelle": "Responsable_Big_Data"},
        {"code": "404288", "libelle": "Developpeur_Data"},
        {"code": "404291", "libelle": "Data_Protection_Officer"},
        {"code": "404939", "libelle": "Biostatisticien_data_manager"},
        {"code": "405222", "libelle": "Data_Analyst_De_La_Performance"},
        {"code": "489091", "libelle": "Database_Administrator"},
    ]

    for item in code_libelle:
        if item["code"] == appellation:
            libelle = item["libelle"]
            break

    print(f"{Fore.GREEN}== Récupération des offres ({appellation}: {libelle}) :")

    output_file = os.path.join(current_directory, "outputs", f"offres_{appellation}_{libelle}.json")

    if os.path.exists(output_file):
        os.remove(output_file)

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    #### Première requête pour voir combien d'offres sont disponibles

    response = requests.get(url, headers=headers, params=filter_params)

    print(f"{Fore.GREEN}==== Récupération des offres (requête 0), pour connaître le nombre d'offres :", end=" ")

    max_offres = int(response.headers.get("Content-Range").split("/")[-1])  # response.headers.get('Content-Range') = offres 0-0/9848

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
                # response = requests.get(url, headers=headers, params=params)
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
        print(f"Status Code : {response.status_code}")
        print(response.text)
        print(response.json())

    print("")
