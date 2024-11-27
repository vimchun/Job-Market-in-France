import json
import os

import requests
import yaml  # pip install pyyaml

CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script (todo: trouver une meilleure solution)


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

    # On renseigne les params conformément à la page suivante :
    # https://francetravail.io/produits-partages/documentation/utilisation-api-france-travail/generer-access-token
    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
    params = {"realm": "/partenaire"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    }

    # requête POST pour obtenir le token
    response = requests.post(url, headers=headers, params=params, data=data)

    print("== Récupération du bearer token :")
    if response.status_code == 200:
        response_json = response.json()
        bearer_token = response_json["access_token"]
        print(f"Status Code: {response.status_code}, bearer token: {bearer_token}\n")
        return bearer_token
    else:
        print(f"Erreur, Status Code: {response.status_code}\n")
        print(f"=> {response.json()}")
        return None


# récupération des credentials données sur le site de FT, depuis un fichier yaml
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)

file_path = os.path.join(current_directory, "..", CREDENTIALS_FILE)

with open(file_path, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(
    client_id=IDENTIFIANT_CLIENT,
    client_secret=CLE_SECRETE,
    scope="o2dsoffre api_offresdemploiv2",  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
)


def get_appellation():
    """
    Récupérer les appellations
    Un "code" correspon à un "libelle", par exemple :

     - { "code": "404278", "libelle": "Data engineer" }

    """
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
        # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)
    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        print(response.text)


# get_appellation()


def get_offres():
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",  # Utilisation du Bearer Token dans l'en-tête
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
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "outputs", "offres.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        print(response.text)
        print(response.json())


get_offres()
