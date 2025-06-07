"""
Temps d'exécution : 20-30 minutes de bout en bout

Ce script est utilisé pour générer un fichier json qui contiendra toutes les anciennes offres et toutes les nouvelles récupérées par API.

Descriptif de ce que fait le script : `readme_pages/step_1__extract_and_transform_data.md`,
  section `Script "api_extract__transform/extract_and_transform_data.py"`
"""

import csv
import os
import shutil
import sys

from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

from colorama import Fore, Style, init

from airflow.decorators import dag, task, task_group
from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

from utils.functions import (
    add_date_extract_attribute,
    add_date_premiere_ecriture_attribute,
    add_location_attributes,
    check_presence_yaml_file,
    concatenate_all_json_into_one,
    count_json_files_number,
    create_csv__code_name__city_department_region,
    create_name_for_concat_json_file,
    get_bearer_token,
    get_offers,
    get_referentiel_appellations_rome,
    get_referentiel_pays,
    keep_only_offres_from_metropole,
    load_code_appellation_yaml_file,
    nb_json_on_setup_0_or_1,
    remove_all_json_files,
    test_a,
    test_b,
)

#### "Partie paramétrable"
# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
#  => Il faut mettre à 1 toutes les variables suivantes pour exécuter le script de bout en bout.
launch_remove_all_get_json_files = 1  # ~ quelques secondes
launch_get_offres = 1  # ~ 20 minutes
launch_concatenate_all_json_into_one = 1  # ~ 1 minute
#
launch_keep_only_offres_from_metropole = 1  # ~ quelques secondes
launch_add_location_attributes = 1  # ~ 5 minutes
launch_add_date_extract_attribute = 1  # ~ quelques secondes
#
launch_concatenate_to_final_json = 1
launch_add_date_premiere_ecriture_attribute = 1
#### Fin "Partie paramétrable"


# Récupération des credentials données sur le site de FT, depuis un fichier yaml
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script
current_directory = os.path.dirname(os.path.abspath(__file__))
credential_filename = os.path.join(current_directory, "..", "data", "resources", CREDENTIALS_FILE)
codes_appellation_filename = os.path.join(current_directory, "..", "data", "resources", "code_appellation_libelle.yml")
json_files_original_from_api_directory = os.path.join(current_directory, "..", "data", "outputs", "offres", "0--original_json_files_from_api")
generated_json_files_directory = os.path.join(current_directory, "..", "data", "outputs", "offres", "1--generated_json_file")

with open(credential_filename, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]


@dag(
    dag_id="projet",
    tags=["projet"],
    schedule_interval=None,
    # start_date=days_ago(0),
)
def my_dag():
    with TaskGroup(group_id="setup_group", tooltip="xxx") as setup:
        with TaskGroup(group_id="check_files_in_folders", tooltip="xxx") as check:
            count = count_json_files_number(directory_path=generated_json_files_directory)  #### task S1
            check_presence_yaml_file(file_path=codes_appellation_filename)  #### task S2

        with TaskGroup(group_id="after_checks", tooltip="xxx") as after_checks:
            remove_all_json_files(json_files_original_from_api_directory)  #### task S3
            token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)  #### task S4
            code_libelle_list = load_code_appellation_yaml_file()  #### task S5
            created_json_filename = create_name_for_concat_json_file()  #### task S6

        check >> after_checks

    with TaskGroup(group_id="etl_group", tooltip="xxx") as etl:
        api_requests = (
            get_offers  #### task A1
            # "partial()" car token commun à toutes les tâches mappées
            .partial(token=token)
            # "expand()" car 1 task par valeur de la liste "code_libelle_list"
            .expand(code_libelle_list=code_libelle_list)
        )

        all_json_in_one = concatenate_all_json_into_one(  #### task A2
            json_files_from_api_directory=json_files_original_from_api_directory,
            generated_json_file_directory=generated_json_files_directory,
            new_json_filename=created_json_filename,
        )

        # metropole = keep_only_offres_from_metropole(  #### task A3
        #     json_files_directory=generated_json_files_directory,
        #     json_filename=created_json_filename,
        #     new_json_filename=created_json_filename,  # on écrase le fichier en entrée
        # )

        # add_location = add_location_attributes(  #### task A4
        #     json_files_directory=generated_json_files_directory,
        #     json_filename=created_json_filename,
        #     new_json_filename=created_json_filename,  # on écrase le fichier en entrée
        # )

        # add_date_extract = add_date_extract_attribute(  #### task A5
        #     json_files_directory=generated_json_files_directory,
        #     json_filename=created_json_filename,
        #     new_json_filename=created_json_filename,  # on écrase le fichier en entrée
        #     date_to_insert=None,  # "None" pour avoir la date du jour
        #     # date_to_insert="2025-03-02"  # pour écraser la valeur si l'attribut est existant dans le json
        # )

        a = test_a()
        b = test_b()

        branch = nb_json_on_setup_0_or_1(count)

        # api_requests >> all_json_in_one >> metropole >> add_location >> add_date_extract
        api_requests >> all_json_in_one >> branch  # >> [a, b]
        branch >> [a, b]


my_dag = my_dag()

# def functions_sequence(json_files_from_api_directory, generated_json_files_directory, json_filename):
#     """
#     Cette fonction exécute les fonctions suivantes à exécuter séquentiellement :
#         - remove_all_json_files()
#         - get_offres()
#         - concatenate_all_json_into_one()
#         - keep_only_offres_from_metropole()
#         - add_location_attributes()
#         - add_date_extract_attribute()

#     si les booléens associés respectifs sont activées :
#         - launch_remove_all_get_json_files
#         - launch_concatenate_all_json_into_one
#         - launch_keep_only_offres_from_metropole
#         - launch_add_location_attributes
#         - launch_add_date_extract_attribute
#     """

#     if launch_remove_all_get_json_files:
#         remove_all_json_files(json_files_original_from_api_directory)
#     ####
#     # if launch_get_offres:
#     #     print(f'{Fore.GREEN}\n==> Fonction "get_offres()"\n')

#     #     with open(codes_appellation_filename, "r") as file:
#     #         content = yaml.safe_load(file)
#     #         code_appellation_libelle = content["code_appellation_libelle"]
#     #         codes_list = [i["code"] for i in code_appellation_libelle]

#     #     for code in codes_list:
#     #         get_offres(token, code_appellation_libelle, filter_params={"appellation": code, "paysContinent": "01"})
#     #         # Note : "paysContinent": "01" pour la France (non restreint à la métropôle)
#     # ####
#     # if launch_concatenate_all_json_into_one:
#     #     concatenate_all_json_into_one(
#     #         json_files_from_api_directory=json_files_from_api_directory,
#     #         generated_json_file_directory=generated_json_files_directory,
#     #         new_json_filename=json_filename,  # on écrase le fichier en entrée
#     #     )
#     #     print(Fore.YELLOW + "Shape : " + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
#     # ####
#     # if launch_keep_only_offres_from_metropole:
#     #     keep_only_offres_from_metropole(
#     #         json_files_directory=generated_json_files_directory,
#     #         json_filename=json_filename,
#     #         new_json_filename=json_filename,  # on écrase le fichier en entrée
#     #     )
#     #     print(Fore.YELLOW + "Shape : " + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
#     # ####
#     # if launch_add_location_attributes:
#     #     add_location_attributes(
#     #         json_files_directory=generated_json_files_directory,
#     #         json_filename=json_filename,
#     #         new_json_filename=json_filename,  # on écrase le fichier en entrée
#     #     )
#     #     print(Fore.YELLOW + "Shape : " + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
#     # ####
#     # if launch_add_date_extract_attribute:
#     #     add_date_extract_attribute(
#     #         json_files_directory=generated_json_files_directory,
#     #         json_filename=json_filename,
#     #         new_json_filename=json_filename,  # on écrase le fichier en entrée
#     #         # date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
#     #         # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
#     #     )
#     #     df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)
#     #     print(f"{Fore.YELLOW}Shape : {df.shape}", f"{Fore.YELLOW}{df.dateExtraction.value_counts()}", sep="\n\n")  # pour investigation


# if 1:
#     # création liste avec tous les fichiers json
#     json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]

#     now = datetime.now().strftime("%Y-%m-%d--%Hh%M")

#     # Le script continue si le dossier "1--generated_json_file" contient 0 ou 1 fichier json

#     if len(json_file_in_generated_directory) == 1:  # en premier car cas le plus fréquent
#         #### Le dossier contient 1 fichier json.
#         current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_1.json

#         # Création d'un nouveau json, créé à partir des nouvelles offres, avec de nouveaux appels API
#         occurence_number = int(Path(current_json_file).stem.split("extraction_occurence_")[1])  # note : stem pour récupérer le nom du fichier sans l'extension
#         new_json_file = f"{now}__extraction_occurence_{occurence_number+1}.json"

#         print(
#             f'Il y a 1 fichier json dans le dossier "{generated_json_files_directory}"',
#             f' -> json_1 = "{Fore.YELLOW}{current_json_file}{Style.RESET_ALL}"',
#             "",
#             f"{Fore.RED}== Lancement de l'extraction occurence {occurence_number+1} ==",
#             f'Création de json_2 = "{Fore.YELLOW}{new_json_file}{Style.RESET_ALL}" à partir de nouvelles requêtes API, qui après traitement sera le seul json qui restera dans le dossier',
#             sep="\n",
#         )

#         functions_sequence(
#             json_files_from_api_directory=json_files_original_from_api_directory,
#             generated_json_files_directory=generated_json_files_directory,
#             json_filename=new_json_file,
#         )

#         if launch_concatenate_to_final_json:
#             print(f"{Fore.RED}\n==> Concaténation entre le json précédemment présent dans le dossier, et le json nouvellement créé\n")
#             df1 = pd.read_json(os.path.join(generated_json_files_directory, current_json_file), dtype=False)
#             df2 = pd.read_json(os.path.join(generated_json_files_directory, new_json_file), dtype=False)

#             #
#             intersection_ids = pd.merge(df1, df2, on="id")["id"].tolist()
#             df1_minus_intersection = df1[~df1.id.isin(intersection_ids)]  # c'est la "partie_1" dans "workflow_db_update.drawio"
#             df_concat = pd.concat([df1_minus_intersection, df2])  # concaténation de "partie_1" et "partie_2" (cf "workflow_db_update.drawio")

#             # print("df1", df1.datePremiereEcriture.value_counts())  # pour investigation
#             # print("df_concat", df_concat.datePremiereEcriture.value_counts())  # pour investigation

#             # Pour faire ce qui est décrit ici "api_extract__transform/outputs/offres/1--generated_json_file/troubleshooting/...
#             #   ...concatenation_dateExtraction_datePremiereEcriture/notes.xlsx" pour l'attribut "datePremiereEcriture".

#             # df_concat.loc[df_concat["id"].isin(df1["id"]), "datePremiereEcriture"] = df1["datePremiereEcriture"]  # pb si les 2 df n'ont pas les mêmes index

#             df_concat.set_index("id", inplace=True)
#             df1.set_index("id", inplace=True)

#             df_concat.loc[df1.index, "datePremiereEcriture"] = df1["datePremiereEcriture"]

#             df_concat.reset_index(inplace=True)

#             # print("df_concat après loc", df_concat.datePremiereEcriture.value_counts())  # pour investigation

#             # print(
#             #     "df1",
#             #     df1[["id", "datePremiereEcriture", "dateExtraction"]],
#             #     "df2",
#             #     df2[["id", "dateExtraction"]],
#             #     "df_concat",
#             #     df_concat,
#             #     sep="\n\n",
#             # )  # pour investigation

#             # Ecriture du nom du fichier et du nombre d'offres dans le fichier "_json_files_history.csv"
#             with open(os.path.join(generated_json_files_directory, "_json_files_history.csv"), "a", newline="") as f:
#                 writer = csv.writer(f)
#                 writer.writerow([new_json_file, len(df_concat)])

#             # Ecriture dans le fichier json
#             df_concat.to_json(
#                 os.path.join(generated_json_files_directory, new_json_file),
#                 orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
#                 force_ascii=False,  # pour convertir les caractères spéciaux
#                 indent=4,  # pour formatter la sortie
#             )

#             # On supprime les backslashs ajoutés par la méthode .to_json()
#             with open(os.path.join(generated_json_files_directory, new_json_file), "r", encoding="utf-8") as f:
#                 content = f.read()

#                 content = content.replace("\\/", "/")  # On remplace "\/" par "/"
#                 content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

#                 # On sauvegarde le fichier final sans les '\'
#                 with open(os.path.join(generated_json_files_directory, new_json_file), "w", encoding="utf-8") as f:
#                     f.write(content)

#             ####
#             if launch_add_date_premiere_ecriture_attribute:
#                 add_date_premiere_ecriture_attribute(
#                     json_files_directory=generated_json_files_directory,
#                     json_filename=new_json_file,
#                     new_json_filename=new_json_file,  # on écrase le fichier en entrée
#                     # date_to_insert="2025-04-10",  # à commenter si on veut mettre la date du jour
#                     # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
#                     overwrite_all_lines=False,
#                 )

#             df = pd.read_json(os.path.join(generated_json_files_directory, new_json_file), dtype=False)

#             print(
#                 f"{Fore.YELLOW}Shape du df1 : {df1.shape}",
#                 f"{Fore.YELLOW}{df1.dateExtraction.value_counts()}",
#                 f"{Fore.YELLOW}{df1.datePremiereEcriture.value_counts()}",
#                 "",
#                 f"{Fore.YELLOW}Shape du df du json concaténé : {df.shape}",
#                 f"{Fore.YELLOW}{df.dateExtraction.value_counts()}",
#                 f"{Fore.YELLOW}{df.datePremiereEcriture.value_counts()}",
#                 sep="\n\n",
#             )  # pour investigation

#             # Le nouveau json a été mis à jour avec la concaténation, il reste à déplacer l'ancien fichier json dans le dossier "archive_json_files"
#             shutil.move(
#                 os.path.join(generated_json_files_directory, current_json_file),
#                 os.path.join(generated_json_files_directory, "archive_json_files", current_json_file),
#             )

#     ####

#     elif not json_file_in_generated_directory:
#         #### Le dossier contient 0 fichier json.
#         print(
#             f'Il n\'y a pas de fichier json dans le dossier "{generated_json_files_directory}"',
#             f"{Fore.RED}== Lancement de l'extraction occurence 1 ==",
#             sep="\n",
#         )

#         json_filename = f"{now}__extraction_occurence_1.json"

#         functions_sequence(
#             json_files_from_api_directory=json_files_original_from_api_directory,
#             generated_json_files_directory=generated_json_files_directory,
#             json_filename=json_filename,
#         )

#         # if launch_add_date_premiere_ecriture_attribute:
#         #     add_date_premiere_ecriture_attribute(
#         #         json_files_directory=generated_json_files_directory,
#         #         json_filename=json_filename,
#         #         new_json_filename=json_filename,  # on écrase le fichier en entrée
#         #         # date_to_insert="2025-04-10",  # à commenter si on veut mettre la date du jour
#         #         # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
#         #         overwrite_all_lines=False,
#         #     )

#         # Ecriture du nom du fichier et du nombre d'offres dans le fichier "_json_files_history.csv"
#         with open(os.path.join(generated_json_files_directory, "_json_files_history.csv"), "a", newline="") as f:
#             writer = csv.writer(f)
#             writer.writerow([json_filename, len(json_filename)])  # todo : len(df) au lieu de len(...) ?

#             ####

#     elif len(json_file_in_generated_directory) > 1:
#         #### Il y a plus d'un fichier, on arrête le script car le dossier doit en contenir 0 ou 1.
#         print(
#             f'Il y a plusieurs fichiers json dans le dossier : "{generated_json_files_directory}" (il n\'en faut que 0 ou 1)',
#             f"{Fore.RED}== Arrêt du script ==",
#             sep="\n",
#         )
#         sys.exit()


# ####
# if 0:
#     """
#     Ce qui suit n'a normalement pas besoin d'être lancé car les fonctions ont déjà générés les fichiers (voir commentaires)
#     On laisse cette partie au cas où ça pourrait servir, par exemple pour mettre à jour un des fichiers.
#     """
#     launch_get_referentiel_appellations_rome = 0  # fichier "appellations_rome.json" déjà généré et poussé
#     launch_get_referentiel_pays = 0  # fichier "pays.json" déjà généré et poussé
#     launch_create_location_csv = 1  # fichier "code_name__city_department_region.csv" déjà généré et poussé

#     if launch_get_referentiel_appellations_rome:
#         get_referentiel_appellations_rome(token)

#     if launch_get_referentiel_pays:
#         get_referentiel_pays(token)

#     if launch_create_location_csv:
#         create_csv__code_name__city_department_region()
