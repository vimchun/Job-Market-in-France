import os

import yaml

from functions import get_bearer_token, get_appellations


# récupération des credentials données sur le site de FT, depuis un fichier yaml
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script (todo: trouver une meilleure solution)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "..", CREDENTIALS_FILE)

with open(file_path, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]


###

token = get_bearer_token(
    client_id=IDENTIFIANT_CLIENT,
    client_secret=CLE_SECRETE,
    scope="o2dsoffre api_offresdemploiv2",  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
)


get_appellations(token)

get_offres(token)
