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
    print(f"{Fore.GREEN}== Récupération du bearer token :{Style.NORMAL}")

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
    print(f"{Fore.GREEN}== Récupération des appellations :{Style.NORMAL}")

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
        print(f"Status Code: {response.status_code}\n")
        # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)

        file_path = os.path.join(current_directory, "outputs", "appellations.json")
        data = response.json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

    return None


def get_offres(token):
    """
    Récupérer les offre et les écrit dans un fichier json.
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Ne retourne rien.
    Possibilité d'ajouter beaucoup de filtres (todo)
    """
    print(f"{Fore.GREEN}== Récupération des offres :{Style.NORMAL}")

    output_file = os.path.join(current_directory, "outputs", "offres.json")

    if os.path.exists(output_file):
        os.remove(output_file)

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Première requête pour voir elle peut retourner combien d'offres
    range_start = 0
    range_end = 0

    params = {
        "range": f"{range_start}-{range_end}",
        "accesTravailleurHandicape": False,
        # "appellation": "404278",  # filtre sur { "code": "404278", "libelle": "Data engineer" },
        "appellation": "10438",  # permet de lancer un test plus rapide car moins d'offres
    }

    response = requests.get(url, headers=headers, params=params)

    print(f"{Fore.GREEN}==== Récupération des offres (requête 1) :{Style.NORMAL}")

    if response.status_code == 200:
        print(f"Status Code: {response.status_code}")
    elif response.status_code == 206:
        print(f"Status Code: {response.status_code} (Réponse partielle)")
        print(f"Plage de contenu: {response.headers.get("Content-Range")}")  ##==> Plage de contenu: offres 0-0/9848

        max_offres = int(response.headers.get("Content-Range").split("/")[-1])
        print(f"Il y a {max_offres+1} offres au total => {int(max_offres/150)+1} requêtes nécessaires (avec 150 documents) pour récupérer toutes les offres.\n")
    else:
        print(f"Erreur lors de la requête API: {response.status_code}")
        print(response.text)
        print(response.json())

    if max_offres == 1:
        pass  # cas à traiter
    elif max_offres < 150:
        # Si on a moins de 150 offres, une seule requête suffit
        print(f"{Fore.GREEN}==== Récupération des offres (requête 2) :{Style.NORMAL}")
        params["range"] = f"{range_start}-{max_offres}"

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(f"Status Code: {response.status_code}")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)

        else:
            print(f"Erreur lors de la requête API: {response.status_code}")
            print(response.text)
            print(response.json())

    else:
        # Si on a plus de 150 offres, il faut faire plusieurs requêtes (une requête renvoie 150 documents max)
        print(f"{Fore.GREEN}==== Récupération des offres (requêtes 2...{2+int(max_offres/150)}) :{Style.NORMAL}")
        range_start = 0
        range_end = 149
        request_id = 2
        params["range"] = f"{range_start}-{range_end}"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("[\n")  # Ajouter un "[" pour "initialiser" le fichier json

        document_id = 0

        for i in range(int(max_offres / 150) + 1):
            # while max_offres >= range_end:
            print(f"{Fore.GREEN}====== Récupération des offres (requête {request_id}) :{Style.NORMAL}", end=" ")
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 206:
                print(f"Status Code: {response.status_code}", end=", ")

                with open(output_file, "a", encoding="utf-8") as f:
                    for obj in response.json()["resultats"]:
                        json.dump(obj, f, ensure_ascii=False)
                        if document_id < max_offres - 1:
                            f.write(",\n")  # Ajouter une virgule après chaque objet
                            # f.write(f",{document_id}\n")  # Ajouter une virgule après chaque objet
                        else:
                            f.write("\n")  # Pour le dernier document, on ne met pas de virgule, sinon le json n'est pas valide
                        document_id += 1
                print(f"{range_start}-{range_end}/{max_offres}")

            else:
                print(f"Status Code: {response.status_code}")  # à investiguer

            range_start += 150
            range_end += 150
            params["range"] = f"{range_start}-{range_end}"
            request_id += 1

        with open(output_file, "a", encoding="utf-8") as f:
            f.write("]")  # Clore le json en ajoutant un crochet fermant "]"


#        # la dernière requête pour avoir les dernières offres
#        print(f"{Fore.GREEN}====== Récupération des offres (requête {request_id}) :{Style.NORMAL}", end=" ")
#        response = requests.get(url, headers=headers, params=params)
#
#        if response.status_code == 206:
#            print(f"Status Code: {response.status_code}")
#
#            with open(output_file, "a", encoding="utf-8") as f:
#                for obj in response.json()["resultats"]:
#                    json.dump(obj, f, ensure_ascii=False)
#                    if document_id < max_offres - 1:
#                        f.write(",\n")  # Ajouter une virgule après chaque objet
#                    else:
#                        f.write("\n")  # Pour le dernier document, on ne met pas de virgule, sinon le json n'est pas valide
#                    document_id += 1
#
#            with open(output_file, "a", encoding="utf-8") as f:
#                f.write("]")  # Clore le json en ajoutant un crochet fermant "]"
#
# import sys

# sys.exit()

# if response.status_code == 200:
#     print(f"Réponse de l'API: {response.status_code}")
# elif response.status_code == 206:
#     print(f"Réponse de l'API: {response.status_code} (Réponse partielle)")
#     print("Plage de contenu:", response.headers.get("Content-Range"))

#     # Ecrire la sortie dans un fichier json
#     file_path = os.path.join(current_directory, "outputs", "offres.json")
#     data = response.json()
#     with open(file_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# else:
#     print(f"Erreur lors de la requête API: {response.status_code}")
#     print(response.text)
#     print(response.json())

# à nettoyer : autres éléments qui permettent de filtrer
# "appellation": "404278, 10438",  # todo : ca a pas l'air de marcher... ça renvoie le même nombre que si on met que le premier élément
# "codeNAF": "",
# "codeROME": "",
# "commune": "",
# "departement": "",
# "distance": "",
# "domaine": "",
# "dureeContratMax": "",
# "dureeContratMin": "",
# "dureeHebdo": "",
# "dureeHebdoMax": "",
# "dureeHebdoMin": "",
# "entreprisesAdaptees": "",
# "experience": "",
# "experienceExigence": "",
# "inclureLimitrophes": "",
# "maxCreationDate": "",
# "minCreationDate": "",
# "modeSelectionPartenaires": "",
# "motsCles": "",
# "natureContrat": "",
# "niveauFormation": "",
# "offresMRS": "",
# "offresManqueCandidats": "",
# "origineOffre": "",
# "partenaires": "",
# "paysContinent": "",
# "periodeSalaire": "",
# "permis": "",
# "publieeDepuis": "",
# "qualification": "",
# "region": "",
# "salaireMin": "",
# "secteurActivite": "",
# "sort": "",
# "tempsPlein": "",
# "theme": "",
# "typeContrat": "",
