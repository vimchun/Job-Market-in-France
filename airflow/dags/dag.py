import os

from datetime import datetime

from utils.functions import (
    add_date_extract_attribute,
    add_date_premiere_ecriture_attribute,
    add_location_attributes,
    concatenate_all_json_into_one,
    count_json_files_number,
    delete_all_in_one_json,
    get_bearer_token,
    get_creds_from_yaml_file,
    get_offers,
    is_existing_appellations_yaml_file,
    is_existing_credentials_yaml_file,
    is_existing_csv_file,
    keep_only_offres_from_metropole,
    load_code_appellation_yaml_file,
    nb_json_on_setup_0_or_1,
    remove_all_json_files,
    rename_json_file,
    special_jsons_concatenation,
    write_to_history_csv_file,
)

from airflow.decorators import dag
from airflow.utils.task_group import TaskGroup

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "..", "data", "resources")
OUTPUTS_DIR = os.path.join(CURRENT_DIR, "..", "data", "outputs")

DOWNLOADED_JSONS_FROM_API_DIR = os.path.join(OUTPUTS_DIR, "offres", "0--original_json_files_from_api")
AGGREGATED_JSON_DIR = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file")

CREDENTIAL_FILENAME = os.path.join(RESOURCES_DIR, "api_credentials_minh.yml")
CODES_APPELLATION_FILENAME = os.path.join(RESOURCES_DIR, "code_appellation_libelle.yml")
LOCATION_CSV_FILENAME = os.path.join(RESOURCES_DIR, "code_name__city_department_region.csv")
AGGREGATED_JSON_FILENAME = "all_in_one.json"

SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/


@dag(
    dag_id="projet_DE",
    tags=["projet"],
    start_date=datetime(2025, 6, 1),  # param obligatoire pour airflow 3.0.1 sinon on n'a pas la grid view associée à ce DAG
    # schedule_interval=None,  # ne pas mettre ce param pour airflow 3.0.1
)
def my_dag():
    with TaskGroup(group_id="SETUP", tooltip="xxx") as setup:
        with TaskGroup(group_id="check_files_in_folders", tooltip="xxx") as check:
            is_existing_csv_file(LOCATION_CSV_FILENAME)  #### task S1
            is_existing_appellations_yaml_file(CODES_APPELLATION_FILENAME)  #### task S1
            is_existing_credentials_yaml_file(CREDENTIAL_FILENAME)  #### task S1

            delete_json = delete_all_in_one_json()  #### task S1
            count = count_json_files_number(AGGREGATED_JSON_DIR)  #### task S1

            delete_json >> count

        with TaskGroup(group_id="after_checks", tooltip="xxx") as after_checks:
            remove_all_json_files(DOWNLOADED_JSONS_FROM_API_DIR)  #### task S2
            code_libelle_list = load_code_appellation_yaml_file()  #### task S2
            dict_ = get_creds_from_yaml_file(CREDENTIAL_FILENAME)  #### task S2
            token = get_bearer_token(dict_, SCOPES_OFFRES)  #### task S2

        check >> after_checks

    with TaskGroup(group_id="ETL", tooltip="xxx") as etl:
        api_requests = get_offers.partial(token=token).expand(code_libelle_list=code_libelle_list)  #### task A1
        # notes : 1/ "partial()" car token commun à toutes les tâches mappées, 2/ "expand()" car 1 task par valeur de la liste "code_libelle_list"

        with TaskGroup(group_id="transforms_and_load_to_json", tooltip="xxx") as tl:
            all_json_in_one = concatenate_all_json_into_one(DOWNLOADED_JSONS_FROM_API_DIR, AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME)  #### task A2

            # note : pour les fonctions suivantes, on prend le fichier "all_in_one_json" et on écrase son contenu.
            metropole = keep_only_offres_from_metropole(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME)  #### task A3
            add_location = add_location_attributes(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME)  #### task A4
            add_date_extract = add_date_extract_attribute(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME, None)  #### task A5
            # notes : 1/ "None" pour avoir la date du jour, 2/ date_to_insert="2025-03-02"  pour écraser la valeur si l'attribut est existant dans le json

            branch = nb_json_on_setup_0_or_1(count)  #### task A6

            all_json_in_one >> metropole >> add_location >> add_date_extract >> branch

            with TaskGroup(group_id="0_json_in_folder", tooltip="xxx") as file0:
                now = datetime.now().strftime("%Y-%m-%d--%Hh%M")
                new_json_filename = f"{now}__extraction_occurence_1.json"

                add_date_first_0 = add_date_premiere_ecriture_attribute(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, AGGREGATED_JSON_FILENAME, None, False)  #### task A8
                json_rename = rename_json_file(AGGREGATED_JSON_DIR, AGGREGATED_JSON_FILENAME, new_json_filename)  #### task A9

                add_date_first_0 >> json_rename

            with TaskGroup(group_id="1_json_in_folder", tooltip="xxx") as file1:
                json_concat_filename = special_jsons_concatenation(AGGREGATED_JSON_DIR)  #### task A7
                add_date_first_1 = add_date_premiere_ecriture_attribute(AGGREGATED_JSON_DIR, json_concat_filename, json_concat_filename, None, False)  #### task A8

                json_concat_filename >> add_date_first_1

            branch >> file0
            branch >> file1

        write_history = write_to_history_csv_file(AGGREGATED_JSON_DIR)  #### task A10

        api_requests >> tl
        [file0, file1] >> write_history

    setup >> etl


my_dag()
