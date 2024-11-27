import json
import os

import requests

from colorama import Back, Fore, Style, init

init(autoreset=True)  # avoid the need to reset the coloring


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

    print(f"{Fore.GREEN}== Récupération du bearer token :{Style.NORMAL}")
    if response.status_code == 200:
        response_json = response.json()
        bearer_token = response_json["access_token"]
        print(f"Status Code: {response.status_code}, bearer token: {bearer_token}\n")
        return bearer_token
    else:
        print(f"Erreur, Status Code: {response.status_code}\n")
        print("oo")
        print(f"=> {response.json()}")
        return None


def get_appellations(token):
    """
    Récupérer les appellations et les écrit dans un fichier json.
    Ne retourne rien.
    Un "code" correspond à un "libelle", par exemple :

     - { "code": "404278", "libelle": "Data engineer" }
    """
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
        print(f"Status Code: {response.status_code}")
        # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)

        file_path = os.path.join(current_directory, "outputs", "appellations.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        print(response.text)

    return None


def get_offres(token):
    """
    Récupérer les offre et les écrit dans un fichier json.
    Ne retourne rien.
    Possibilité d'ajouter beaucoup de filtres (todo)
    """
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    params = {
        "appellation": "404278",
    }

    response = requests.get(url, headers=headers, params=params)

    print("== Récupération des offres :")

    if response.status_code == 200:
        print(f"Réponse de l'API: {response.status_code}")
    if response.status_code == 206:
        print(f"Réponse de l'API: {response.status_code} (Réponse partielle)")
        print("Plage de contenu:", response.headers.get("Content-Range"))

        # Ecrire la sortie dans un fichier json
        file_path = os.path.join(current_directory, "outputs", "offres.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        print(response.text)
        print(response.json())
