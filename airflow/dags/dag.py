import os

from datetime import datetime

import yaml

from colorama import Fore, Style, init

from airflow.decorators import dag
from airflow.utils.task_group import TaskGroup

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

from utils.functions import (
    add_date_extract_attribute,
    add_date_premiere_ecriture_attribute,
    add_location_attributes,
    check_presence_yaml_file,
    concatenate_all_json_into_one,
    count_json_files_number,
    get_bearer_token,
    get_offers,
    keep_only_offres_from_metropole,
    load_code_appellation_yaml_file,
    nb_json_on_setup_0_or_1,
    remove_all_json_files,
    rename_json_file,
    special_jsons_concatenation,
    write_to_history_csv_file,
)

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

now = datetime.now().strftime("%Y-%m-%d--%Hh%M")
all_in_one_json = "all_in_one.json"


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
            new_json_filename=all_in_one_json,
        )

        metropole = keep_only_offres_from_metropole(  #### task A3
            json_files_directory=generated_json_files_directory,
            json_filename=all_in_one_json,
            new_json_filename=all_in_one_json,  # on écrase le fichier en entrée
        )

        add_location = add_location_attributes(  #### task A4
            json_files_directory=generated_json_files_directory,
            json_filename=all_in_one_json,
            new_json_filename=all_in_one_json,  # on écrase le fichier en entrée
        )

        add_date_extract = add_date_extract_attribute(  #### task A5
            json_files_directory=generated_json_files_directory,
            json_filename=all_in_one_json,
            new_json_filename=all_in_one_json,  # on écrase le fichier en entrée
            date_to_insert=None,  # "None" pour avoir la date du jour
            # date_to_insert="2025-03-02"  # pour écraser la valeur si l'attribut est existant dans le json
        )

        branch = nb_json_on_setup_0_or_1(count)  #### task A6

        api_requests >> all_json_in_one >> metropole >> add_location >> add_date_extract >> branch

        with TaskGroup(group_id="0_json_in_folder", tooltip="xxx") as file0:
            add_date_first_0 = add_date_premiere_ecriture_attribute(  #### task A8
                json_files_directory=generated_json_files_directory,
                json_filename=all_in_one_json,
                new_json_filename=all_in_one_json,
                date_to_insert=None,
                overwrite_all_lines=False,
            )

            new_json_filename = f"{now}__extraction_occurence_1.json"

            json_rename = rename_json_file(  #### task A9
                json_files_directory=generated_json_files_directory,
                json_filename=all_in_one_json,
                new_json_filename=new_json_filename,
            )

            branch >> add_date_first_0 >> json_rename

        with TaskGroup(group_id="1_json_in_folder", tooltip="xxx") as file1:
            json_concat_filename = special_jsons_concatenation(generated_json_files_directory=generated_json_files_directory)  #### task A7

            add_date_first_1 = add_date_premiere_ecriture_attribute(  #### task A8
                json_files_directory=generated_json_files_directory,
                json_filename=json_concat_filename,
                new_json_filename=json_concat_filename,
                date_to_insert=None,
                overwrite_all_lines=False,
            )

            branch >> json_concat_filename >> add_date_first_1

        write_history = write_to_history_csv_file(generated_json_files_directory=generated_json_files_directory)  #### task A10

        [file0, file1] >> write_history


my_dag = my_dag()
