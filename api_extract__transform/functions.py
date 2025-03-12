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


def remove_all_json_files(json_files_directory):
    """
    Supprime tous les fichiers json du dossier spécifié
    """

    print(f'{Fore.GREEN}\n==> Fonction "remove_all_json_files()"\n')

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

    print(f'{Fore.GREEN}\n==> Fonction "get_offres()"\n')

    appellation = filter_params["appellation"]

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
            # output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}_{libelle}.json")
            output_file = os.path.join(current_directory, "outputs", "offres", "original_json_files_from_api", f"{appellation}_{libelle}.json")

        else:
            # output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}__{max_offres}_offres.json")
            # output_file = os.path.join(current_directory, "outputs", "offres", f"{appellation}.json")
            output_file = os.path.join(current_directory, "outputs", "offres", "original_json_files_from_api", f"{appellation}.json")

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

    print(f'{Fore.GREEN}\n==> Fonction "concatenate_all_into_one()"\n')

    df_concat = pd.DataFrame()

    for filename in os.listdir(json_files_directory):
        if filename.endswith(".json") and filename != concat_json_filename:  # traite aussi le cas du fichier sans extension
            print(filename)
            try:
                # si le json est bien valide
                with open(os.path.join(json_files_directory, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                df = pd.DataFrame(data)
                # df_concat = pd.concat([df, df_concat], ignore_index=True)
                df_concat = pd.concat([df_concat, df], ignore_index=True)

            except json.JSONDecodeError as e:
                print(f"{Fore.RED}Erreur 1 lors du chargement du fichier JSON {filename} : {e}")
            except FileNotFoundError:
                print(f'{Fore.RED}Le fichier "{filename}" n\'a pas été trouvé.')
            except Exception as e:
                print(f"{Fore.RED}Une erreur inattendue s'est produite : {e}")

    print(f"\n --> df_concat : {df_concat.shape[0]} offres, df_concat_drop_duplicates : {df_concat.drop_duplicates(['id']).shape[0]} offres")

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

    # On remplace les deux-points sans espace par des deux-points avec espace
    content = content.replace('":', '": ')

    # On sauvegarde le fichier final sans les '\'
    with open(os.path.join(json_files_directory, concat_json_filename), "w", encoding="utf-8") as f:
        f.write(content)

    return df_concat.drop_duplicates(["id"])


def keep_only_offres_from_metropole(json_files_directory, json_filename):
    """
    Cette fonction écrase le json entré en paramètre, en ne conservant que les offres d'emploi de la France Métropolitaine.
    Elle ne conserve pas les offres de la Corse ni des DOMTOM.

    Ne retourne rien.
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
    list_departements = [
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
        # "Nouvelle-Aquitaine",  # pour tester
    ]

    df_lieu_norm_metropole = df_lieu_norm_metropole[~df_lieu_norm_metropole["libelle"].isin(list_departements)]  # .value_counts(subset="libelle")

    ## On réécrit le json initial avec uniquement les offres en métropole
    # On réécrit un nouveau json avec uniquement les offres en métropole

    new_json = f"{json_filename.split("__0__all")[0]}.json"  # pour avoir seulement "2025-03-12--10h21.json"

    df[df["id"].isin(df_lieu_norm_metropole["id"])].to_json(
        # os.path.join(json_files_directory, json_filename),
        os.path.join(json_files_directory, new_json),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )  # fonctionne bien mais ajoute des backslashs pour échapper les slashs

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_files_directory, new_json), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")

        # On remplace les deux-points sans espace par des deux-points avec espace
        content = content.replace('":', '": ')

        # Récupération le nombre de documents pour l'écrire dans le nom du nouveau fichier
        json_data = json.loads(content)
        num_json_documents = len(json_data)
        # print(num_json_documents)

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(json_files_directory, new_json), "w", encoding="utf-8") as f:
            f.write(content)

    # On renomme le fichier de sortie pour avoir par exemple : "2025-03-05--22h09__1__only_metropole_13419_offres.json"
    os.rename(
        os.path.join(json_files_directory, new_json),
        os.path.join(json_files_directory, f"{new_json[:-5]}__1__only_metropole_{num_json_documents}_offres.json"),
    )

    # Définir le chemin du nouveau fichier
    # new_json_filename = "nouveau_fichier.json"  # Remplacez par le nom du fichier que vous souhaitez créer

    # Ouvrir le nouveau fichier en mode écriture
    # with open(os.path.join(json_files_directory, f"{json_filename.split('__')[0]}.json"), "w", encoding="utf-8") as f:
    #     f.write(content)

    #    # Définir le chemin du nouveau fichier
    #    new_json_filename = "nouveau_fichier.json"  # Remplacez par le nom du fichier que vous souhaitez créer
    #
    #    # Ouvrir le nouveau fichier en mode écriture
    #    with open(os.path.join(json_files_directory, new_json_filename), "w", encoding="utf-8") as f:
    #        f.write(content)

    return None


def create_csv__code_name__city_department_region():
    """
    Créé à partir du notebook "1--create_csv_codes__city_departement_region.ipynb".
    Génère le fichier "Job_Market/additional_files/code_name__city_department_region" qui sert à récupérer les informations suivantes :

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

    import os

    import pandas as pd

    print(f'{Fore.GREEN}\n==> Fonction "create_csv__code_name__city_department_region()"\n')

    # todo : ajouter la partie download / unzip des fichiers (pas urgent)

    # Fichiers du lien_2
    # ==================

    current_directory = os.path.dirname(os.path.abspath(__file__))

    files_directory = os.path.join(
        current_directory,
        "..",
        "additional_files",
        "archives",
    )
    file_commune = "v_commune_2024.csv"
    file_departement = "v_departement_2024.csv"
    file_region = "v_region_2024.csv"

    # df_commune
    # ==========

    df_commune = pd.read_csv(
        os.path.join(files_directory, "lien_2", file_commune),
        usecols=[
            "COM",
            "REG",
            "DEP",
            "LIBELLE",
        ],
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
            "..",
            "additional_files",
            # "code_name__city_department_region",
            "code_name__city_department_region.csv",
        ),
        index=False,  # pour ne pas écrire les index
    )

    # pd.read_csv(
    #     os.path.join(
    #         current_directory,
    #         "..",
    #         "additional_files",
    #         "code_name__city_department_region",
    #     ),
    #     dtype=str,
    # )


def add_location_attributes(json_path, json_original_file, json_generated_file):
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

    Ne retourne rien.
    """
    import os
    import time

    import numpy as np
    import pandas as pd
    import unidecode

    from geopy.geocoders import Nominatim

    print(f'{Fore.GREEN}\n==> Fonction "add_location_attributes()"\n')

    # Chargement des fichiers
    # =======================

    print(f'\n====> Chargement des fichiers"\n')

    df = pd.read_json(
        os.path.join(json_path, json_original_file),
        dtype=False,  # désactiver l'inférence des types
    )

    df_insee = pd.read_csv(
        os.path.join(
            os.path.join("..", "additional_files"),
            "code_name__city_department_region.csv",
        ),
        dtype=str,
    )

    lieuTravail_normalized = pd.json_normalize(df["lieuTravail"])

    df = df.join(lieuTravail_normalized)

    df_lieu = df[["id", "intitule"] + list(lieuTravail_normalized.columns)]

    df_lieu.rename(
        {
            "codePostal": "code_postal",
            "commune": "code_insee",
        },
        axis=1,
        inplace=True,
    )

    # Cas_1 : "code_insee" renseigné
    # ==============================
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
    print(len(df_lieu[(df_lieu.lieu_cas == "cas_1") & (df_lieu.nom_ville.isna())]) == 0)
    assert len(df_lieu[(df_lieu.lieu_cas == "cas_1") & (df_lieu.nom_ville.isna())]) == 0

    import sys

    sys.exit()

    ###################################################################################################################

    # Cas_2 : "code_insee = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées
    # ==============================================================================================

    print(f'\n====> Cas_2 : "code_insee = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées\n')

    # %% [markdown]
    # ### <u> Récupération code_postal avec geopy </u>

    # %%
    # df_lieu[~df_lieu.lieu_cas.isin(["cas_1"])  # != cas_1
    #     & ~df_lieu.latitude.isna()
    #         ]  # fmt: off

    # %%

    geolocator = Nominatim(user_agent="my_geopy_app")

    # %%
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
            row["lieu_cas"] = "cas_2_coordonnées_gps_hors_FR"

        # Géocodage avec retry
        retries = 0
        while retries < max_retries:
            try:
                location = geolocator.reverse((row["latitude"], row["longitude"]), language="fr", exactly_one=True)
                if location:
                    address = location.raw.get("address", {})
                    row["code_postal"] = address.get("postcode", "Inconnu")
                else:
                    row["code_postal"] = "Inconnu"
                break  # on sort de la boucle si succès

            except Exception as e:
                retries += 1
                print(f"Erreur pour ({row['latitude']}, {row['longitude']}), tentative {retries}/{max_retries}: {e}")
                if retries < max_retries:
                    time.sleep(retry_delay)
                else:
                    row["code_postal"] = "Erreur geocodage"

        return row

    # %%
    # df_lieu

    # %%
    # cas_2 sans .apply() -> pas de code postal
    # df_lieu[
    #     ~df_lieu.lieu_cas.isin(["cas_1"])  # != cas_1
    #     & ~df_lieu.latitude.isna()
    # ].head(2)

    # %%
    # /!\ temps d'exécution de plusieurs minutes
    cas_2 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1"])  # != cas_1
        & ~df_lieu.latitude.isna()
    ].apply(check_and_swap, axis=1)

    # %%
    cas_2  # .head(2)  # code_postal retourné par geopy
    # cas_2.shape

    # %%
    cas_2[cas_2.id == "2347948"]

    # %% [markdown]
    # ### <u> suite geopy </u>

    # %% [markdown]
    # #### <u> Merge df_geopy et df_insee </u>

    # %%
    cas_2_geopy = cas_2.copy()

    # %%
    # cas_2_geopy.shape

    # %%
    # avant de merger avec df_insee, on supprime les colonnes qui n'ont que des NAN
    cas_2_geopy = cas_2_geopy.drop(["code_insee", "nom_commune", "nom_ville", "code_departement", "nom_departement", "code_region", "nom_region"], axis=1)

    # %%
    # cas_2_geopy.head(2)
    # cas_2_geopy.shape

    # %%
    # df_insee.head(2)

    # %%
    cas_2_geopy_merge = cas_2_geopy.merge(df_insee, on="code_postal", how="left").drop_duplicates("id")

    # %%
    # cas_2_geopy_merge  # .head(2)

    # %%
    # cas_2_geopy_merge.shape

    # %% [markdown]
    # #### <u> Gestion des cas où code_postal non reconnu </u>

    # %% [markdown]
    # Parfois le code postal retourné par geopy n'est pas présent dans le fichier "code_name__city_department_region"
    #
    # Dans ce cas, on va prendre les 2 premiers digits du code postal pour avoir le département, et récupérer la région.
    #

    # %%
    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge[cas_2_geopy_merge.code_insee.isna()]

    # %%
    # cas_2_geopy_merge_unknown_CP

    # %%
    # Les 2 premiers digits du CP pour le code_departement.
    # cas_2_geopy_merge_unknown_CP.code_departement = cas_2_geopy_merge_unknown_CP.apply(lambda x: x.code_postal[:2], axis=1)
    cas_2_geopy_merge_unknown_CP.loc[:, "code_departement"] = cas_2_geopy_merge_unknown_CP["code_postal"].apply(lambda x: x[:2])

    # %%
    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge_unknown_CP.drop(["code_insee", "nom_commune", "nom_ville", "nom_departement", "code_region", "nom_region"], axis=1)  # avec le code_departement

    # %%
    # cas_2_geopy_merge_unknown_CP

    # %%
    # df_insee[["code_departement", "nom_departement", "code_region", "nom_region"]].head(2)

    # %%
    cas_2_geopy_merge_unknown_CP = cas_2_geopy_merge_unknown_CP.merge(df_insee[["code_departement", "nom_departement", "code_region", "nom_region"]], on="code_departement").drop_duplicates("id")

    # %%
    # cas_2_geopy_merge_unknown_CP

    # %% [markdown]
    # #### <u> Update df </u>

    # %% [markdown]
    # On peut updater le df précédent

    # %%
    # cas_2_geopy_merge.head(6)

    # %%
    # cas_2_geopy_merge_unknown_CP

    # %%
    # Pour vérifier : ici, "code_departement = nom_departement = code_region = nom_region = NAN"
    # cas_2_geopy_merge[cas_2_geopy_merge.code_insee.isna()]

    # %%
    # Modification pour avoir id en tant qu'index, nécessaire pour que .update() fonctionne (car .update() ne fonctionne que sur l'index du df)
    cas_2_geopy_merge.set_index("id", inplace=True)
    cas_2_geopy_merge_unknown_CP.set_index("id", inplace=True)

    cas_2_geopy_merge.update(cas_2_geopy_merge_unknown_CP)
    cas_2_geopy_merge.reset_index(inplace=True)

    # %%
    # Pour vérifier : ici, "code_departement = nom_departement = code_region = nom_region" sont bien mise à jour
    # cas_2_geopy_merge[cas_2_geopy_merge.code_insee.isna()]

    # %%
    cas_2_geopy_merge_unknown_CP

    # %%
    # cas_2_geopy_merge.shape

    # %%
    # cas_2_geopy_merge.head(2)

    # %%
    cas_2_geopy_merge

    # %% [markdown]
    # #### <u> Update de df_lieu avec cas_2_geopy_merge </u>

    # %%
    # df_lieu.head(2)

    # %%
    # Vérification avant update : pas de cas_2
    df_lieu[df_lieu.lieu_cas == "cas_2"]

    # %%
    # Modification pour avoir id en tant qu'index, nécessaire pour que .update() fonctionne (car .update() ne fonctionne que sur l'index du df)
    cas_2_geopy_merge.set_index("id", inplace=True)
    df_lieu.set_index("id", inplace=True)

    df_lieu.update(cas_2_geopy_merge)

    df_lieu.reset_index(inplace=True)

    # %%
    # Vérification avant update : cas_2 avec les colonnes de localisation mises à jour
    df_lieu[df_lieu.lieu_cas == "cas_2"]

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_2"].shape

    # %%
    # df_lieu.shape

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_1"].shape

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_2"].shape

    # %% [markdown]
    # -----------------------

    # %% [markdown]
    # ### <u> Problèmes ? </u>
    ### Vérification

    # %%
    # df_lieu[(df_lieu.lieu_cas == "cas_2") & (df_lieu.nom_departement.isna())]

    # %% [markdown]
    # => pas de problème

    # %% [markdown]

    ###################################################################################################################

    # ## <u> Cas_3 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = 'numéro_département - nom_département'" </u>

    print(f'\n====> Cas_3 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = numéro_département - nom_département"\n')

    # %%
    cas_3 = df_lieu[~df_lieu.lieu_cas.isin(["cas_1", "cas_2"])  # != cas_1/2
                & df_lieu.libelle.str.match(r"^\d{2}\s-\s")
                    ]  # fmt: off

    # %%
    # cas_3

    # %%
    # cas_3.shape

    # %%
    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_3.id), "lieu_cas"] = "cas_3"

    # %%
    # df_lieu.value_counts("lieu_cas")

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_3"].head(2)

    # %% [markdown]
    ### Ajout attributs ville/département/région

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_3"].code_departement = df_lieu[df_lieu.lieu_cas == "cas_3"].apply(lambda x: x.libelle.split(" - ")[0], axis=1)
    df_lieu.loc[df_lieu.lieu_cas == "cas_3", "code_departement"] = df_lieu.loc[df_lieu.lieu_cas == "cas_3", "libelle"].apply(lambda x: x.split(" - ")[0])

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_3"].head(2)

    # %% [markdown]
    # ### <u> Update de df_lieu </u>

    # %%
    # df_insee.head(2)

    # %%
    df_insee_cas_3 = df_insee[["code_departement", "nom_departement", "code_region", "nom_region"]].drop_duplicates()

    # %%
    # df_insee_cas_3.head(2)

    # %%
    # récupération des noms de colonnes de df_lieu pour restaurer l'ordre des colonnes après .reset_index()
    columns_order = df_lieu.columns

    # %%
    df_lieu.set_index("code_departement", inplace=True)
    df_insee_cas_3.set_index("code_departement", inplace=True)

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_3"].head(2)

    # %%
    # df_insee_cas_3.head(2)

    # %%
    df_lieu.update(df_insee_cas_3)

    # %%
    df_lieu.reset_index(inplace=True)

    # %%
    df_lieu = df_lieu[columns_order]

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_3"]

    # %%
    # df_lieu

    # %% [markdown]
    # ### <u> Problèmes ? </u>
    ### Vérification

    # %%
    df_lieu[(df_lieu.lieu_cas == "cas_3") & (df_lieu.nom_departement.isna())]

    # %% [markdown]
    # ==> pas de problème

    # %% [markdown]

    ###################################################################################################################

    # Cas_4 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = nom_région"
    # ============================================================================================

    print(f'\n====> Cas_4 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = nom_région"\n')

    # %%
    cas_4 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3"])  # != cas_1/2/3
        & ~df_lieu.libelle.isin(["FRANCE", "France", "France entière"])
    ]

    # cas_4.value_counts("libelle")
    # note:
    # Ile-de-France                 23   <=== i sans accent circonflexe
    # Île-de-France                  4   <=== i accent circonflexe
    # =>

    # %%
    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_4.id), "lieu_cas"] = "cas_4"

    # %%
    # df_lieu.lieu_cas.value_counts()

    # %% [markdown]
    ### Ajout attributs ville/département/région

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_4"].head(2)

    # %% [markdown]
    # Avant d'appliquer .update() :
    #
    # - On met le nom des régions de la colonne "libelle" en minuscule.
    # - On remplace les tirets par des espaces.
    # - On enlève les accents avec la lib unidecode
    #

    # %%
    df_lieu.loc[:, "libelle_traite"] = df_lieu["libelle"]

    # %%
    # df_lieu.head(2)

    # %%

    df_lieu.loc[df_lieu.lieu_cas == "cas_4", "libelle_traite"] = df_lieu.loc[df_lieu.lieu_cas == "cas_4", "libelle"].apply(lambda x: unidecode.unidecode(x).lower().replace("-", " "))  # , axis=1)

    # %%
    df_lieu[df_lieu.lieu_cas == "cas_4"]

    # %%
    df_insee_cas_4_update_1 = df_insee.copy()

    # %%
    df_insee_cas_4_update_1.nom_region = df_insee.nom_region.apply(lambda x: unidecode.unidecode(x).lower().replace("-", " "))

    # %%
    df_insee_cas_4_update_1 = df_insee_cas_4_update_1[["code_region", "nom_region"]].drop_duplicates()

    # %%
    df_insee_cas_4_update_1.rename({"nom_region": "libelle_traite"}, axis=1, inplace=True)  # pour pouvoir faire le .update()

    # %%
    df_insee_cas_4_update_1

    # %% [markdown]
    # ### <u> Update 1 </u>

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_4"].head(2)

    # %%
    # df_insee_cas_4_update_1.head(2)

    # %%
    df_lieu.set_index("libelle_traite", inplace=True)

    # %%
    df_insee_cas_4_update_1.set_index("libelle_traite", inplace=True)

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_4"].head(2)

    # %%
    # df_insee_cas_4_update_1

    # %%
    df_lieu.update(df_insee_cas_4_update_1)

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_4"].head()

    # %% [markdown]
    # ### <u> Update 2 </u>

    # %%
    df_lieu.set_index("code_region", inplace=True)

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_4"].head()

    # %%
    df_insee_cas_4_update_2 = df_insee.copy()

    # %%
    df_insee_cas_4_update_2 = df_insee_cas_4_update_2[["code_region", "nom_region"]].drop_duplicates()

    # %%
    # df_insee_cas_4_update_2

    # %%
    df_insee_cas_4_update_2.set_index("code_region", inplace=True)

    # %%
    # df_insee_cas_4_update_2

    # %%
    df_lieu.update(df_insee_cas_4_update_2)

    # %%
    df_lieu.reset_index(inplace=True)

    # %%
    # columns_order

    # %%
    df_lieu = df_lieu[columns_order]

    # %%
    df_lieu[(df_lieu.lieu_cas == "cas_4")].head(100)

    # %% [markdown]
    # ### <u> Problèmes ? </u>
    ### Vérification

    # %% [markdown]
    # ==> pas de problème

    # %% [markdown]
    ###################################################################################################################

    # Cas_5 : "code_postal = code_insee = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"
    # ====================================================================================================================

    print(f'\n====> Cas_5 : "code_postal = code_insee = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"\n')

    # %%
    cas_5 = df_lieu[
        ~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3", "cas_4"])  # != cas_1/2/3/4
        & df_lieu.libelle.isin(["FRANCE", "France", "France entière"])
    ]

    # %%
    cas_5

    # %%
    # On écrit le numéro du cas dans "lieu_cas"
    df_lieu.loc[df_lieu.id.isin(cas_5.id), "lieu_cas"] = "cas_5"

    # %%
    # df_lieu.lieu_cas.value_counts()

    # %%

    df_lieu.loc[df_lieu.lieu_cas == "cas_5", "libelle"] = np.nan

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_5"].value_counts("libelle")

    # %%
    # df_lieu[df_lieu.lieu_cas == "cas_5"]

    # %% [markdown]
    # ## <u> Vérification qu'il n'y a pas d'autres cas </u>

    # %%
    # On vérifie qu'il n'y a aucune autre cas que les cas 1, 2, 3, 4 et 5.
    assert len(df_lieu[~df_lieu.lieu_cas.isin(["cas_1", "cas_2", "cas_3", "cas_4", "cas_5"])]) == 0  # != cas_1/2/3/4/5

    # %%
    # df_lieu.value_counts("lieu_cas")

    # %% [markdown]

    # Update du df initial avec df_lieu
    # =================================

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
    #
    #

    # %%
    df_lieu[df_lieu.lieu_cas == "cas_1"].head()

    # %%
    # On supprime "intitule" car il est déjà dans le Dataframe "df", et "libelle"/"latitude"/"longitude" qui ne nous intéressent plus
    df_lieu = df_lieu.drop(
        [
            "intitule",
            "libelle",
            "latitude",
            "longitude",
        ],
        axis=1,
    )

    # %%
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

    # %%
    # On supprime la colonne "lieuTravail" qui ne nous intéresse plus dorénavant, et les attributs de cette colonne
    df = df.drop(
        [
            "lieuTravail",
            "libelle",
            "latitude",
            "longitude",
            "codePostal",
            "commune",
        ],
        axis=1,
    )

    # %%
    # display(
    #     df.shape,
    #     df_lieu.shape,
    # )

    # %%
    df_final = pd.merge(left=df, right=df_lieu, on="id")

    # %%
    # df_final

    # %% [markdown]
    # Ecriture dans un fichier .json
    # ==============================

    # %%
    df_final.to_json(
        os.path.join(json_path, json_generated_file),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(json_path, json_generated_file), "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("\\/", "/")

    # On remplace les deux-points sans espace par des deux-points avec espace
    content = content.replace('":', '": ')

    # On sauvegarde le fichier final sans les '\'
    with open(os.path.join(json_path, json_generated_file), "w", encoding="utf-8") as f:
        f.write(content)

    # %%
    # df_final.shape
