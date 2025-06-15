import json
import os

from datetime import datetime

import psycopg2

from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup

conn_id = "my_pg"  # nom du "Connection ID" défini dans la GUI d'Airflow

DB_PARAM = {"database": "francetravail", "host": "postgres_3_0_1", "user": "mhh", "password": "mhh", "port": 5432}  # note : "host" != "localhost"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(CURRENT_DIR, "..", "data", "outputs")

AGGREGATED_JSON_DIR = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file")
SPLIT_JSONS_DIR = os.path.join(AGGREGATED_JSON_DIR, "split_json_files")

sql_safe_null = "Ceci est un string qui figure nulle part dans le json pour pouvoir écrire les NULL sans doublon"  # ne peut pas être "-" car cette valeur peut exister


@task(task_id="check_only_one_json_in_folder")
def check_only_one_json_file_in_folder(folder):
    """
    Retourne le chemin du nom du fichier json dans le dossier "folder" s'il n'y a qu'un fichier json dans ce dossier.
    Sinon, s'il y a 0 ou plusieurs fichiers json, on arrête le script.
    """
    json_files = [file for file in os.listdir(folder) if file.endswith(".json")]
    if len(json_files) == 1:
        return os.path.join(folder, json_files[0])
    else:
        raise Exception(f'Il y a {len(json_files)} fichier(s) json dans le dossier "{folder}": {json_files}')


@task(task_id="remove_all_split_jsons")
def remove_all_split_jsons(folder):
    """
    Supprime tous les fichiers json du dossier spécifié
    """
    for file in os.listdir(folder):
        file_to_delete = os.path.join(folder, file)

        if os.path.isfile(file_to_delete):  # vérifie si c'est un fichier
            try:
                os.remove(file_to_delete)
            except Exception as e:
                print(f"Erreur lors de la suppression de {file_to_delete}: {e}")

    return None


@task(task_id="split_large_json")
def split_large_json(filename):
    """
    Charge le json "filename" qui est un gros fichier (plusieurs centaines de MB et qui grandit à chaque itération), et split en plusieurs jsons dédiés pour les fonctions suivantes du DAG.
    L'utilité de cette fonction est que toutes les fonctions suivantes du DAG 1/ ne lise pas le même gros fichier json, 2/ lise chacun son fichier json dédié.

    Ne retoure rien.
    """

    # création du dossier de sortie où on écrira les nouveaux fichiers json
    os.makedirs(SPLIT_JSONS_DIR, exist_ok=True)

    with open(filename, "r") as file:
        offres = json.load(file)

    offre_emploi = []
    contrat = []
    entreprise = []
    localisation = []
    description_offre = []
    competence = []

    for offre in offres:
        offre_id = offre.get("id")

        #### pour "offre_emploi"
        date_actualisation_raw = offre.get("dateActualisation")  # rare cas où `"dateActualisation": null` (1 cas sur 50k à l'occurence 7, offre_id 6985803)
        offre_emploi.append(
            {
                # "offre_id": offre.get("id"),
                "offre_id": offre_id,
                "date_extraction": offre.get("dateExtraction"),
                "date_premiere_ecriture": offre.get("datePremiereEcriture"),
                "date_creation": offre.get("dateCreation").split("T")[0],  # inutile de récupérer l'heure
                "date_actualisation": date_actualisation_raw.split("T")[0] if date_actualisation_raw else None,
                "nombre_postes": offre.get("nombrePostes"),
            }
        )

        #### pour "contrat"
        contrat.append(
            {
                # "offre_id": offre.get("id"),
                "offre_id": offre_id,
                "type_contrat": offre.get("typeContrat"),
                "type_contrat_libelle": offre.get("typeContratLibelle"),
                "duree_travail_libelle": offre.get("dureeTravailLibelle"),
                "duree_travail_libelle_converti": offre.get("dureeTravailLibelleConverti"),
                "nature_contrat": offre.get("natureContrat"),
                "salaire_libelle": offre.get("salaire").get("libelle"),
                "salaire_complement_1": offre.get("salaire").get("complement1"),
                "salaire_complement_2": offre.get("salaire").get("complement2"),
                "salaire_commentaire": offre.get("salaire").get("commentaire"),
                "alternance": offre.get("alternance"),
                "deplacement_code": offre.get("deplacementCode"),
                "deplacement_libelle": offre.get("deplacementLibelle"),
                "temps_travail": offre.get("complementExercice"),
                "condition_specifique": offre.get("conditionExercice"),
            }
        )

        #### pour "entreprise"
        entreprise.append(
            {
                # "offre_id": offre.get("id"),
                "offre_id": offre_id,
                "nom_entreprise": offre.get("entreprise").get("nom"),
                "description_entreprise": offre.get("entreprise").get("description"),
                "code_naf": offre.get("codeNAF"),
                "secteur_activite_libelle": offre.get("secteurActiviteLibelle"),
                "entreprise_adaptee": offre.get("entreprise").get("entrepriseAdaptee"),
            }
        )

        #### pour "localisation"
        entreprise.append(
            {
                # "offre_id": offre.get("id"),
                "offre_id": offre_id,
                "intitule_offre": offre.get("intitule"),
                "description_offre": offre.get("description"),
                "nom_partenaire": offre.get("origineOffre").get("partenaires", [{}])[0].get("nom"),
                "rome_code": offre.get("romeCode"),
                "rome_libelle": offre.get("romeLibelle"),
                "appellation_rome": offre.get("appellationlibelle"),
                "difficile_a_pourvoir": offre.get("offresManqueCandidats"),
                "accessible_travailleurs_handicapes": offre.get("accessibleTH"),
            }
        )

    # Sauvegarde dans des "petits" fichiers json dédiés
    with open(os.path.join(SPLIT_JSONS_DIR, "offre_emploi.json"), "w") as f:
        json.dump(offre_emploi, f)

    with open(os.path.join(SPLIT_JSONS_DIR, "contrat.json"), "w") as f:
        json.dump(contrat, f)

    with open(os.path.join(SPLIT_JSONS_DIR, "entreprise.json"), "w") as f:
        json.dump(entreprise, f)

    with open(os.path.join(SPLIT_JSONS_DIR, "localisation.json"), "w") as f:
        json.dump(localisation, f)


def load_json(filename):
    """
    Charge simplement le json
    Cette fonction ne peut pas être une task, car xcom n'est pas conçu pour stocker des objects volumineux.
    """
    with open(filename, "r") as file:
        return json.load(file)


def create_and_execute_insert_query(table_name: str, row_data: dict, conflict_columns: list, cursor):
    """
    https://www.postgresql.org/docs/current/sql-insert.html

    Insère ou met à jour une ligne dans une table PostgreSQL.

    Paramètres :
      - table_name (str) : nom de la table
      - row_data (dict) : données à insérer (clé = colonne, valeur = donnée)
      - conflict_columns (list) : liste des colonnes utilisées pour "ON CONFLICT"
      - cursor : cursor psycopg2


    Exemple :

        offre_id = "188VMCV"
        date_extraction = "2025-06-15"
        nombre_postes = 3

        fill_db(
            db_table="OffreEmploi",
            row_data={
                "offre_id": offre_id,
                "date_extraction": date_extraction,
                "nombre_postes": nombre_postes,
            },
            conflict_columns=["offre_id"],
            cursor,
        )

                <==>

        cursor.execute(
            f'''--sql
                INSERT INTO OffreEmploi (offre_id, date_extraction, nombre_postes)
                VALUES (%s, %s, %s)
                ON CONFLICT (offre_id) DO UPDATE SET
                    date_extraction = EXCLUDED.date_extraction,
                    nombre_postes = EXCLUDED.nombre_postes
                ''',
            (offre_id, date_extraction, nombre_postes),
        )


    Ne retourne rien
    """

    columns = list(row_data.keys())
    values = list(row_data.values())

    columns_str = ", ".join(columns)  # pour avoir "attribut1, attribut2, ..." sans les quotes
    placeholders = ", ".join(["%s"] * len(columns))  # pour avoir "%s, %s, ..." (1* "%s" par colonne)

    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT ({", ".join(conflict_columns)})
    """

    update_columns = [f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_columns]
    if update_columns:
        query += f" DO UPDATE SET {', '.join(update_columns)}"
    else:
        query += " DO NOTHING"

    cursor.execute(query, values)


@task(task_id="table_offre_emploi")
def insert_into_offre_emploi(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table OffreEmploi"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("offre_id"),
                    "date_extraction": offre.get("date_extraction"),
                    "date_premiere_ecriture": offre.get("date_premiere_ecriture"),
                    "date_creation": offre.get("date_creation"),
                    "date_actualisation": offre.get("date_actualisation"),
                    "nombre_postes": offre.get("nombre_postes"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                create_and_execute_insert_query(table_name="OffreEmploi", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="table_contrat")
def insert_into_contrat(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Contrat"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("offre_id"),
                    "type_contrat": offre.get("type_contrat"),
                    "type_contrat_libelle": offre.get("type_contrat_libelle"),
                    "duree_travail_libelle": offre.get("duree_travail_libelle"),
                    "duree_travail_libelle_converti": offre.get("duree_travail_libelle_converti"),
                    "nature_contrat": offre.get("nature_contrat"),
                    "salaire_libelle": offre.get("salaire_libelle"),
                    "salaire_complement_1": offre.get("salaire_complement_1"),
                    "salaire_complement_2": offre.get("salaire_complement_2"),
                    "salaire_commentaire": offre.get("salaire_commentaire"),
                    "alternance": offre.get("alternance"),
                    "deplacement_code": offre.get("deplacement_code"),
                    "deplacement_libelle": offre.get("deplacement_libelle"),
                    "temps_travail": offre.get("temps_travail"),
                    "condition_specifique": offre.get("condition_specifique"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                create_and_execute_insert_query(table_name="Contrat", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="table_entreprise")
def insert_into_entreprise(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Entreprise"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("offre_id"),
                    "nom_entreprise": offre.get("nom_entreprise"),
                    "description_entreprise": offre.get("description_entreprise"),
                    "code_naf": offre.get("code_naf"),
                    "secteur_activite_libelle": offre.get("secteur_activite_libelle"),
                    "entreprise_adaptee": offre.get("entreprise_adaptee"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                create_and_execute_insert_query(table_name="Entreprise", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="table_localisation")
def insert_into_localisation(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Localisation"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("offre_id"),
                    "code_insee": offre.get("code_insee"),
                    "nom_commune": offre.get("nom_commune"),
                    "code_postal": offre.get("code_postal"),
                    "nom_ville": offre.get("nom_ville"),
                    "code_departement": offre.get("code_departement"),
                    "nom_departement": offre.get("nom_departement"),
                    "code_region": offre.get("code_region"),
                    "nom_region": offre.get("nom_region"),
                    "lieu_cas": offre.get("lieu_cas"),
                    # "offre_id": offre.get("id"),
                    # "code_insee": offre.get("code_insee"),
                    # "nom_commune": offre.get("nom_commune"),
                    # "code_postal": offre.get("code_postal"),
                    # "nom_ville": offre.get("nom_ville"),
                    # "code_departement": offre.get("code_departement"),
                    # "nom_departement": offre.get("nom_departement"),
                    # "code_region": offre.get("code_region"),
                    # "nom_region": offre.get("nom_region"),
                    # "lieu_cas": offre.get("lieu_cas"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                create_and_execute_insert_query(table_name="Localisation", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="table_description_offre")
def insert_into_description_offre(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Description_Offre"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("id"),
                    "intitule_offre": offre.get("intitule"),
                    "description_offre": offre.get("description"),
                    "nom_partenaire": offre.get("origineOffre").get("partenaires", [{}])[0].get("nom"),
                    "rome_code": offre.get("romeCode"),
                    "rome_libelle": offre.get("romeLibelle"),
                    "appellation_rome": offre.get("appellationlibelle"),
                    "difficile_a_pourvoir": offre.get("offresManqueCandidats"),
                    "accessible_travailleurs_handicapes": offre.get("accessibleTH"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                create_and_execute_insert_query(table_name="DescriptionOffre", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="table_competence")
def insert_into_competence(json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Competence"""

    offres = load_json(json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                competences = offre.get("competences")  # ⛔ Attention on a une liste de compétences dans le json !!!

                if competences:
                    print("competence")
                    for i in range(len(competences)):
                        # /!\ note : il faut remplacer NULL par quelque chose (cas "competence_code = null")
                        # /!\  (sinon risque d'écriture de doublon car "NULL != NULL selon la logique SQL")
                        # /!\ à la suite de la boucle, on remplacera ces nouvelles valeurs par les "null"

                        values_dict = {
                            "competence_code": competences[i].get("code", 0),
                            "competence_libelle": competences[i].get("libelle", sql_safe_null),
                            "competence_code_exigence": competences[i].get("exigence", sql_safe_null),
                        }

                        # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation

                        create_and_execute_insert_query(
                            table_name="Competence", row_data=values_dict, conflict_columns=["competence_code", "competence_libelle", "competence_code_exigence"], cursor=cursor
                        )


with DAG(
    dag_id="DAG_2_WRITE_TO_DB_v1",
    tags=["project"],
    start_date=datetime(2025, 6, 1),  # param obligatoire pour airflow 3.0.1 sinon on n'a pas la grid view associée à ce DAG
) as dag:
    with TaskGroup(group_id="SETUP", tooltip="xxx") as setup:
        create_tables = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="create_all_tables_if_not_existing",
            sql=os.path.join("sql", "create_all_tables.sql"),
        )
        json_file_path = check_only_one_json_file_in_folder(AGGREGATED_JSON_DIR)

        remove_all_split_jsons(SPLIT_JSONS_DIR)
        split_large_json(json_file_path)

    with TaskGroup(group_id="WRITE_TO_DATABASE", tooltip="xxx") as write:
        with TaskGroup(group_id="INSERT_TO_TABLES", tooltip="xxx") as insert:
            insert_into_offre_emploi(os.path.join(SPLIT_JSONS_DIR, "offre_emploi.json"))
            insert_into_contrat(os.path.join(SPLIT_JSONS_DIR, "contrat.json"))
            insert_into_entreprise(os.path.join(SPLIT_JSONS_DIR, "entreprise.json"))
            insert_into_localisation(os.path.join(SPLIT_JSONS_DIR, "localisation.json"))
            # insert_into_description_offre(json_file_path)
            # insert_into_competence(json_file_path)

    setup >> write
