import os
import shutil
import sys

from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

from colorama import Fore, init

init(autoreset=True)  # pour colorama, inutile de reset si on colorie
from functions import (
    add_date_extract_attribute,
    add_location_attributes,
    concatenate_all_json_into_one,
    create_csv__code_name__city_department_region,
    get_bearer_token,
    get_offres,
    get_referentiel_appellations_rome,
    get_referentiel_pays,
    keep_only_offres_from_metropole,
    remove_all_json_files,
)

current_directory = os.path.dirname(os.path.abspath(__file__))
generated_json_files_directory = os.path.join(current_directory, "outputs", "offres", "1--generated_json_file")


# création liste avec tous les fichiers json
json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]

today = datetime.now().strftime("%Y-%m-%d--%Hh%M")

# On continue le script si le dossier contient 0 ou 1 fichier json.
# if len(json_file_in_generated_directory) == 1:  # en premier car cas le plus fréquent
if 1:  # en premier car cas le plus fréquent
    # Le dossier contient 1 fichier json.
    current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_0.json

    # On renomme le fichier json en mettant à jour la date et l'heure et on incrémente le numéro de l'occurence dans le nom du fichier

    # occurence_number = int(Path(current_json_file).stem.split("extraction_occurence_")[1])  # note : stem pour récupérer le nom du fichier sans l'extension
    # occurence_number += 1

    # json_filename = f"{today}__extraction_occurence_{occurence_number}.json"
    json_filename_1 = "2025-04-03--18h36__extraction_occurence_12.json"

    # print(
    #     f'Il y a 1 fichier json ("{current_json_file}") dans le dossier "{generated_json_files_directory}"',
    #     "",
    #     f"{Fore.RED}== Lancement de l'extraction occurence {occurence_number} ==",
    #     f'Nouveau nom fichier json : "{json_filename}"',
    #     sep="\n",
    # )

    json_filename_2 = "2025-04-03--23h40__extraction_occurence_13.json"
    json_filename_concat = "concat.json"

    df1 = pd.read_json(os.path.join(generated_json_files_directory, json_filename_1), dtype=False)
    df2 = pd.read_json(os.path.join(generated_json_files_directory, json_filename_2), dtype=False)

    #
    intersection_ids = pd.merge(df1, df2, on="id")["id"].tolist()

    df1_minus_intersection = df1[~df1.id.isin(intersection_ids)]

    df_concat = pd.concat([df1_minus_intersection, df2])

    # print(
    #     df1_minus_intersection.shape,
    #     df2.shape,
    #     df_concat,
    # )

    df_concat.to_json(
        os.path.join(generated_json_files_directory, json_filename_concat),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(generated_json_files_directory, json_filename_concat), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(generated_json_files_directory, json_filename_concat), "w", encoding="utf-8") as f:
            f.write(content)

    # à faire à la fin :
    # archive de l'ancien fichier avant de le renommer et de le traiter
    # shutil.copy(
    #     os.path.join(generated_json_files_directory, current_json_file),
    #     os.path.join(generated_json_files_directory, "archive_json_files", current_json_file),
    # )
    # os.rename(
    #     os.path.join(generated_json_files_directory, current_json_file),
    #     os.path.join(generated_json_files_directory, json_filename),
    # )

elif not json_file_in_generated_directory:
    # Le dossier contient 0 fichier json.
    print(
        f'Il n\'y a pas de fichier json dans le dossier "{generated_json_files_directory}"',
        f"{Fore.RED}== Lancement de l'extraction occurence 1 ==",
        sep="\n",
    )

    json_filename_1 = f"{today}__extraction_occurence_1.json"

elif len(json_file_in_generated_directory) > 1:
    # Il y a plus d'un fichier, on arrête le script car le dossier doit en contenir 0 ou 1.
    print(
        f'Il y a plusieurs fichiers json dans le dossier : "{generated_json_files_directory}" (il n\'en faut que 0 ou 1)',
        f"{Fore.RED}== Arrêt du script ==",
        sep="\n",
    )
    sys.exit()


# today = datetime.now().strftime("%Y-%m-%d--%Hh%M")
# json_filename = f"{today}__extraction_occurence_0.json"  # Pour ne pas le hardcoder
# json_filename = "2025-04-02--14h40__extraction__occurence_0.json"  # Pour le hardcoder

#### "Partie paramétrable"
# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
launch_get_referentiel_appellations_rome = 0  # fichier "appellations_rome.json" déjà généré et poussé (pas utile de relancer)
launch_get_referentiel_pays = 0  # fichier "pays.json" déjà généré et poussé (pas utile de relancer)
launch_create_location_csv = 0  # fichier "code_name__city_department_region.csv" déjà généré et poussé (pas utile de relancer)
#
#  Notes :  - Il faut mettre à 1 toutes les variables suivantes pour exécuter le script de bout en bout.
#           - S'il n'y a pas de commentaire, la fonction met quelques secondes d'exécution.
#
launch_remove_all_get_json_files = 0  # ~ quelques secondes
launch_get_offres = 0  # ~ 20 minutes
launch_concatenate_all_json_into_one = 0  # ~ 1 minute
launch_add_date_extract_attribute = 0  # ~ quelques secondes
launch_keep_only_offres_from_metropole = 0  # ~ quelques secondes
launch_add_location_attributes = 0  # ~ 5 minutes
#### Fin "Partie paramétrable"


# Récupération des credentials données sur le site de FT, depuis un fichier yaml
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script
credential_filename = os.path.join(current_directory, CREDENTIALS_FILE)
json_files_original_from_api_directory = os.path.join(current_directory, "outputs", "offres", "0--original_json_files_from_api")

with open(credential_filename, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)
# token = ""  # lors des tests pour éviter de faire une requête


if launch_get_referentiel_appellations_rome:
    get_referentiel_appellations_rome(token)

if launch_get_referentiel_pays:
    get_referentiel_pays(token)

if launch_remove_all_get_json_files:
    remove_all_json_files(json_files_original_from_api_directory)

if launch_create_location_csv:
    create_csv__code_name__city_department_region()

#################################################################################################################################

if launch_get_offres:
    print(f'{Fore.GREEN}\n==> Fonction "get_offres()"\n')

    credential_filename = os.path.join(current_directory, "code_appellation_libelle.yml")

    with open(credential_filename, "r") as file:
        content = yaml.safe_load(file)
        code_appellation_libelle = content["code_appellation_libelle"]  # functions.py
        codes_list = [i["code"] for i in code_appellation_libelle]

    for code in codes_list:
        get_offres(token, code_appellation_libelle, filter_params={"appellation": code, "paysContinent": "01"})
        # Note : "paysContinent": "01" pour la France (non restreint à la métropôle)

#################################################################################################################################

if launch_concatenate_all_json_into_one:
    concatenate_all_json_into_one(
        json_files_from_api_directory=json_files_original_from_api_directory,
        generated_json_file_directory=generated_json_files_directory,
        new_json_filename=json_filename_1,  # on écrase le fichier en entrée
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename_1), dtype=False).shape))

#################################################################################################################################

if launch_add_date_extract_attribute:
    add_date_extract_attribute(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename_1,
        new_json_filename=json_filename_1,  # on écrase le fichier en entrée
        # date_to_insert="2025-03-22",  # à commenter si on veut mettre la date du jour
        # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename_1), dtype=False)
    print(f'{Fore.YELLOW}{df.shape}   -   Valeur de "dateExtraction" pour le premier document json : {df.loc[1, "dateExtraction"]}')

#################################################################################################################################

if launch_keep_only_offres_from_metropole:
    keep_only_offres_from_metropole(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename_1,
        new_json_filename=json_filename_1,  # on écrase le fichier en entrée
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename_1), dtype=False).shape))

#################################################################################################################################

if launch_add_location_attributes:
    add_location_attributes(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename_1,
        new_json_filename=json_filename_1,
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename_1), dtype=False).shape))
