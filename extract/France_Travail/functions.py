import json
import os
import re

import requests

from colorama import Fore, Style, init
from unidecode import unidecode

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


def get_offres(token, filter_params):
    """
    Récupérer les offre et les écrit dans un fichier json.
    Une requête retourne au maximum 150 offres (cf paramètres range), donc il faut en faire plusieurs s'il y a plus de 150 offres.
    Beaucoup de paramètres possibles, dont le paramètre range qui limite le nombre d'offres retourné à 3150

    Ne retourne rien.
    """

    # current_directory = os.path.dirname(os.path.abspath(__file__))

    # Recherche le "libelle" correspondant à "l'appellation"
    code_libelle = [  # modification du libelle pour pouvoir renommer les fichiers de sortie
        {"code": "38970", "libelle": "Data_Miner"},
        {"code": "38971", "libelle": "Data_Analyst"},
        {"code": "38972", "libelle": "Data_Scientist"},
        {"code": "38975", "libelle": "Data_Manager"},
        {"code": "38977", "libelle": "Developpeur_Big_Data"},
        {"code": "38095", "libelle": "Analyste_Decisionnel_Business_Intelligence"},
        {"code": "404274", "libelle": "Ingenieur_Data_Scientist"},
        {"code": "404276", "libelle": "Architecte_Big_Data"},
        {"code": "404277", "libelle": "Big_Data_Engineer"},
        {"code": "404278", "libelle": "Data_Engineer"},
        {"code": "404279", "libelle": "Docteur_Big_Data"},
        {"code": "404280", "libelle": "Expert_Big_Data"},
        {"code": "404281", "libelle": "Expert_Technique_Big_Data"},
        {"code": "404282", "libelle": "Ingenieur_Big_Data"},
        {"code": "404283", "libelle": "Ingenieur_Dataviz"},
        {"code": "404285", "libelle": "Ingenieur_En_Developpement_Big_Data"},
        {"code": "404286", "libelle": "Responsable_Architecture_Conception_Data"},
        {"code": "404287", "libelle": "Responsable_Big_Data"},
        {"code": "404288", "libelle": "Developpeur_Data"},
        {"code": "404291", "libelle": "Data_Protection_Officer"},
        {"code": "404939", "libelle": "Biostatisticien_Data_Manager"},
        {"code": "405222", "libelle": "Data_Analyst_De_La_Performance"},
        {"code": "489091", "libelle": "Database_Administrator"},
        {"code": "404275", "libelle": "Analyste_Qualite_Des_Donnees"},
        {"code": "404289", "libelle": "Analyste_Scientifique_Des_Donnees"},
        {"code": "404271", "libelle": "Expert_En_Sciences_Des_Donnees"},
        {"code": "404273", "libelle": "Explorateur_De_Donnees"},
        {"code": "404284", "libelle": "Ingenieur_Donnees"},
        {"code": "404289", "libelle": "Analyste_Scientifique_Des_Donnees"},
    ]

    codes_list = [i["code"] for i in code_libelle]

    appellation = filter_params["appellation"]

    libelle = ""

    for item in code_libelle:
        if item["code"] == appellation:
            libelle = item["libelle"]
            break

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


def filtrer_offres_selon_dictionnaire(directory, strings_a_verifier_dans_intitule, output_filename):
    """
    Rappel : La fonction get_offres() génèrent des fichiers json selon les appellations rentrées en paramètres.
    La fonction courante :
        - parse ces fichiers json :
          - en conservant que les offres dont les intitulés contiennent les strings spécifiés
            parmi les valeurs de la clé "a_inclure" du dictionnaire passé en argument,
          - en retirant les offres dont les intitulés contiennent les strings spécifiés
            parmi les valeurs de la clé "a_exclure" du dictionnaire passé en argument,
        - écrit ces offres dans un json
    """

    offres_id_filtered = []
    doc_nb = 1

    output_file = os.path.join(current_directory, "outputs", "offres", "offres_filtered", output_filename)

    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "a", encoding="utf-8") as f:
        f.write("[\n")

        for filename in os.listdir(directory):
            if filename.endswith(".json") and filename != output_filename:  # traite aussi le cas du fichier sans extension
                try:
                    # si le json est bien valide
                    with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                        data = json.load(file)
                        for line in data:
                            offre_id = line["id"]
                            intitule = line["intitule"]
                            date_creation = line["dateCreation"].split("T")[0]
                            date_actualisation = line["dateActualisation"].split("T")[0]
                            lieu = line["lieuTravail"]["libelle"]
                            nom_entreprise = line.get("entreprise", {}).get("nom", "-")  # "{}" pour renvoyer un dictionnaire vide si la clé "entreprise" n'existe pas  # fmt:skip #noqa

                            # print(f"\n{Fore.GREEN}-> intitulé : {intitule}")  # [utile pour investigation]
                            for inclu in strings_a_verifier_dans_intitule["a_inclure"]:
                                if len(inclu.split(" ")) == 1:
                                    mot = unidecode(inclu.split(" ")[0].lower())
                                    # print(f"{Fore.YELLOW}pattern : {mot}", end=" => ")  # [utile pour investigation]

                                    condition_1 = re.search(mot, unidecode(intitule.lower()))
                                    condition_3 = all(
                                        not re.search(unidecode(exclu.lower()), unidecode(intitule.lower()))
                                        for exclu in strings_a_verifier_dans_intitule["a_exclure"]
                                    )

                                    if condition_1 and condition_3:
                                        # print("oui")  # [utile pour investigation]
                                        if offre_id not in offres_id_filtered:
                                            offres_id_filtered.append(offre_id)
                                            print(f"{filename.split('_')[0]:<8} n°{doc_nb:<5} id:{offre_id}  {intitule:<85} {date_creation}   {date_actualisation}   {lieu:30}   {nom_entreprise}")  # fmt:skip  # noqa
                                            if doc_nb != 1:
                                                f.write(",\n")
                                            json.dump(line, f, ensure_ascii=False)
                                            doc_nb += 1
                                        break
                                    # else:  # [utile pour investigation]
                                    #     print("non")  # [utile pour investigation]

                                elif len(inclu.split(" ")) == 2:
                                    mot_1 = unidecode(inclu.split(" ")[0].lower())
                                    mot_2 = unidecode(inclu.split(" ")[1].lower())
                                    pattern_1 = f"{mot_1}(.*?){mot_2}"  # regex
                                    pattern_2 = f"{mot_2}(.*?){mot_1}"  # regex
                                    # print(f"{Fore.YELLOW}patterns : {pattern_1} | {pattern_2}", end=" => ")  # [utile pour investigation]
                                    condition_1 = re.search(pattern_1, unidecode(intitule.lower()))
                                    condition_2 = re.search(pattern_2, unidecode(intitule.lower()))
                                    condition_3 = all(
                                        not re.search(unidecode(exclu.lower()), unidecode(intitule.lower()))
                                        for exclu in strings_a_verifier_dans_intitule["a_exclure"]
                                    )

                                    if (condition_1 and condition_3) or (condition_2 and condition_3):
                                        # print("oui")  # [utile pour investigation]
                                        if offre_id not in offres_id_filtered:
                                            offres_id_filtered.append(offre_id)
                                            print(f"{filename.split('_')[0]:<8} n°{doc_nb:<5} id:{offre_id}  {intitule:<85} {date_creation}   {date_actualisation}   {lieu:30}   {nom_entreprise}")  # fmt:skip  # noqa
                                            if doc_nb != 1:
                                                f.write(",\n")
                                            json.dump(line, f, ensure_ascii=False)
                                            doc_nb += 1
                                        break
                                    # else: # [utile pour investigation]
                                    #     print("non")  # [utile pour investigation]

                except json.JSONDecodeError as e:
                    print(f"{Fore.RED}Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
                except FileNotFoundError:
                    print(f'{Fore.RED}Le fichier "{filename}" n\'a pas été trouvé.')
                except Exception as e:
                    print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")

        f.write("\n]")

    try:
        with open(output_file, "r", encoding="utf-8") as file:
            data = json.load(file)  # todo: ajouter des assertions ?
            print(f'{Fore.GREEN}Le fichier généré "{output_filename}" est bien un json valide.')
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Erreur 2 lors du chargement du fichier JSON {output_file} : {e}")
    except FileNotFoundError:
        print(f'{Fore.RED}Le fichier "{output_filename}" n\'a pas été trouvé.')
    except Exception as e:
        print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")
