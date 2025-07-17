import json
import logging
import os

from datetime import timedelta

import psycopg2

from airflow import DAG
from airflow.decorators import task
from airflow.models.dag import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.task_group import TaskGroup

conn_id = "connection_postgres"  # nom du "Connection ID" défini

DB_PARAM = {"database": "francetravail", "host": "postgres", "user": "mhh", "password": "mhh", "port": 5432}  # note : "host" != "localhost"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(CURRENT_DIR, "..", "data", "outputs")

AGGREGATED_JSON_DIR = os.path.join(OUTPUTS_DIR, "offres", "1--generated_json_file")
SPLIT_JSONS_DIR = os.path.join(AGGREGATED_JSON_DIR, "split_json_files")


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


def get_token():
    """
    Récupère le bearer token pour pouvoir faire les requêtes pour GET et POST les connections.
    """

    import requests

    response = requests.post(
        "http://airflow-apiserver:8080/auth/token",
        json={"username": "airflow", "password": "airflow"},
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()  # lève une exception si erreur

    return response.json()["access_token"]


@task(task_id="ensure_postgres_connexion")
def ensure_postgres_connexion(postgres_connection_name):
    """
    Vérifie que la connexion postgres nommée "postgres_connection_name" existe, et la crée le cas échéant (comme si on le faisait depuis la GUI d'Airflow).
    """

    import requests

    token = get_token()

    for _ in range(2):
        """
        Boucle pour itérer 2 fois uniquement (pour éviter un while), pour :
        1. GET connection
        2. Si existe avec bons params => break
        3. Sinon DELETE connection + création connection => continue
        4. Si création OK => break
        """

        # Requête pour récupérer les informations de la connection nommée "postgres_connection_name"
        response = requests.get(
            url=f"http://airflow-apiserver:8080/api/v2/connections/{postgres_connection_name}",
            headers={"Authorization": f"Bearer {token}"},
        )

        print("** Informations connections existantes **")
        print("   - status_code :", response.status_code)
        print("   - text :", response.text)  # string

        conn_dict_to_create = {
            "connection_id": postgres_connection_name,
            "conn_type": "postgres",
            "description": "Connection créée avec DAG 2",
            "host": "postgres",
            "login": "mhh",
            "password": "mhh",
            "port": 5432,
            "schema": "francetravail",
            "extra": None,
        }

        if response.status_code == 200:
            current_connection_json = json.loads(response.text)  # on passe le string en dict

            # On compare certains champs des 2 jsons pour s'assurer que la connection "postgres_connection_name" a les bons paramètres
            fields_to_compare = ["conn_type", "description", "host", "login", "port", "schema"]

            subset_current = {k: current_connection_json[k] for k in fields_to_compare}
            subset_to_create = {k: conn_dict_to_create[k] for k in fields_to_compare}

            if subset_current != subset_to_create:
                print(f'La connection "{postgres_connection_name}" existe déjà mais les paramètres ne sont pas comme ceux désirés.')

                response_delete = requests.delete(
                    url=f"http://airflow-apiserver:8080/api/v2/connections/{postgres_connection_name}",
                    headers={"Authorization": f"Bearer {token}"},
                )

                print("** Suppression de la connection (car paramètres différents de ceux désirés) **")
                print("   - status_code :", response_delete.status_code)
                print("   - text :", response_delete.text)

                continue  # on passe à l'occurence suivante de la boucle for

            print(f'La connection "{postgres_connection_name}" existe déjà avec les bons paramètres.')

            break  # on sort de la boucle for, si pas de problème au niveau comparaison des params

        elif response.status_code == 401:
            raise ValueError("Token invalide (Unauthorized).")

        elif response.status_code == 404:
            print(f'==> La connection "{postgres_connection_name}" n\'existe pas, on va la créer.')
            response_post = requests.post(
                url="http://airflow-apiserver:8080/api/v2/connections",
                json=conn_dict_to_create,
                headers={"Authorization": f"Bearer {token}"},
            )

            print(f'** Création de la connection "{postgres_connection_name}" **')
            print("   - status_code :", response_post.status_code)
            print("   - text :", response_post.text)

            if response_post.status_code != 201:  # 201 si la connection est bien crée
                raise ValueError(f'La connection "{postgres_connection_name}" n\'est pas bien créée.')

            break  # on sort de la boucle for

        else:
            print(f"Status code: {response.status_code}")
            print(f"Response text : {response.text}")

            raise ValueError(f'Problème avec la connection "{postgres_connection_name}"')


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
                logging.error(f"Erreur lors de la suppression de {file_to_delete}: {e}")

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

    # initialisation de listes
    offreemploi = []  # pour la table de fait
    contrat, entreprise, localisation, descriptionoffre, competence, offre_competence = [], [], [], [], [], []  # pour les tables de dimension sans table de fait
    experience, offre_experience = [], []
    formation, offre_formation = [], []
    qualiteprofessionnelle, offre_qualiteprofessionnelle = [], []
    qualification, offre_qualification = [], []
    langue, offre_langue = [], []
    permisconduire, offre_permisconduire = [], []

    # utilisation d'un "set" pour ne pas écrire de doublon dans le json (beaucoup de doublons ici sans l'attribut "offre_id")
    # note : grâce à ces "sets", plus besoin d'utiliser de placeholder pour les placeholders par des NULLs, étant donné qu'on s'assure en amont qu'on n'a pas de doublon.
    (
        seen_competence,
        seen_experience,
        seen_formation,
        seen_qualiteprofessionnelle,
        seen_qualification,
        seen_langue,
        seen_permisconduire,
    ) = [set() for _ in range(7)]

    def strip_and_quote(string_):
        """
        Retourne le string strip (en supprimant les leading et trailing whitespaces, sans espace à gauche et à droite), en entourant par des guillemets.
        S'applique aux VARCHAR (voir "create_all_tables.sql").
        """
        return f'"{string_.strip()}"' if string_ else None

    for offre in offres:
        offre_id = offre.get("id")

        #### pour "offreemploi"
        date_actualisation_raw = offre.get("dateActualisation")  # rare cas où `"dateActualisation": null` (1 cas sur 50k à l'occurence 7, offre_id 6985803)
        offreemploi.append(
            {
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
                "offre_id": offre_id,
                "type_contrat": strip_and_quote(offre.get("typeContrat")),
                "type_contrat_libelle": strip_and_quote(offre.get("typeContratLibelle")),
                "duree_travail_libelle": strip_and_quote(offre.get("dureeTravailLibelle")),
                "duree_travail_libelle_converti": strip_and_quote(offre.get("dureeTravailLibelleConverti")),
                "nature_contrat": strip_and_quote(offre.get("natureContrat")),
                "salaire_libelle": strip_and_quote(offre.get("salaire").get("libelle")),
                "salaire_complement_1": strip_and_quote(offre.get("salaire").get("complement1")),
                "salaire_complement_2": strip_and_quote(offre.get("salaire").get("complement2")),
                "salaire_commentaire": strip_and_quote(offre.get("salaire").get("commentaire")),
                "alternance": offre.get("alternance"),
                "deplacement_code": offre.get("deplacementCode"),
                "deplacement_libelle": strip_and_quote(offre.get("deplacementLibelle")),
                "temps_travail": strip_and_quote(offre.get("complementExercice")),
                "condition_specifique": strip_and_quote(offre.get("conditionExercice")),
            }
        )

        #### pour "entreprise"
        entreprise.append(
            {
                "offre_id": offre_id,
                "nom_entreprise": strip_and_quote(offre.get("entreprise").get("nom")),
                "description_entreprise": strip_and_quote(offre.get("entreprise").get("description")),
                "code_naf": offre.get("codeNAF"),
                "secteur_activite_libelle": strip_and_quote(offre.get("secteurActiviteLibelle")),
                "entreprise_adaptee": offre.get("entreprise").get("entrepriseAdaptee"),
            }
        )

        #### pour "localisation"
        localisation.append(
            {
                "offre_id": offre_id,
                "code_insee": offre.get("code_insee"),  # sur 5 chars
                "nom_commune": strip_and_quote(offre.get("nom_commune")),
                "code_postal": offre.get("code_postal"),  # sur 5 chars
                "nom_ville": strip_and_quote(offre.get("nom_ville")),
                "code_departement": offre.get("code_departement"),  # sur 3 chars
                "nom_departement": strip_and_quote(offre.get("nom_departement")),
                "code_region": offre.get("code_region"),  # sur 2 chars
                "nom_region": strip_and_quote(offre.get("nom_region")),
                "lieu_cas": offre.get("lieu_cas"),  # sur 5 chars
            }
        )

        #### pour "descriptionoffre"
        descriptionoffre.append(
            {
                "offre_id": offre_id,
                "intitule_offre": strip_and_quote(offre.get("intitule")),
                "description_offre": strip_and_quote(offre.get("description")),  # todo : à mettre dans une table à part car trop gros ?
                "nom_partenaire": strip_and_quote(offre.get("origineOffre").get("partenaires", [{}])[0].get("nom")),
                "rome_code": offre.get("romeCode"),  # sur 5 chars
                "rome_libelle": strip_and_quote(offre.get("romeLibelle")),
                "appellation_rome": strip_and_quote(offre.get("appellationlibelle")),
                "difficile_a_pourvoir": offre.get("offresManqueCandidats"),
                "accessible_travailleurs_handicapes": offre.get("accessibleTH"),
            }
        )

        #### pour "competence" / "offre_competence"
        competences = offre.get("competences")  # ⛔ Attention on a une liste de compétences dans le json !!!

        if competences:
            for c in competences:
                values = (
                    c.get("code", 0),
                    c.get("libelle", None),
                    c.get("exigence", None),
                )

                # pour "offre_competence"
                offre_competence.append(
                    {
                        "offre_id": offre_id,
                        "competence_code": values[0],
                        "competence_libelle": strip_and_quote(values[1]),
                        "competence_code_exigence": values[2],
                        "date_extraction": offre.get("dateExtraction"),
                    }
                )

                # pour "competence"
                if values not in seen_competence:
                    seen_competence.add(values)
                    competence.append(
                        {
                            "competence_code": values[0],
                            "competence_libelle": strip_and_quote(values[1]),
                            "competence_code_exigence": values[2],
                        }
                    )

        #### pour "experience" / "offre_experience"
        values = (
            offre.get("experienceLibelle", None),
            offre.get("experienceExige", None),
            offre.get("experienceCommentaire", None),
        )

        # pour "offre_experience"
        offre_experience.append(
            {
                "offre_id": offre_id,
                "experience_libelle": strip_and_quote(values[0]),
                "experience_code_exigence": values[1],
                "experience_commentaire": strip_and_quote(values[2]),
                "date_extraction": offre.get("dateExtraction"),
            }
        )

        # pour "experience"
        if values not in seen_experience:
            seen_experience.add(values)
            experience.append(
                {
                    "experience_libelle": strip_and_quote(values[0]),
                    "experience_code_exigence": values[1],
                    "experience_commentaire": strip_and_quote(values[2]),
                }
            )

        #### pour "formation" / "offre_formation"
        formations = offre.get("formations", [{}])  # ⛔ Attention on a une liste de formations dans le json !!!

        if formations:
            for f in formations:
                values = (
                    f.get("codeFormation", 0),
                    f.get("domaineLibelle", None),
                    f.get("niveauLibelle", None),
                    f.get("commentaire", None),
                    f.get("exigence", None),
                )
                # pour "offre_formation"

                offre_formation.append(
                    {
                        "offre_id": offre_id,
                        "formation_code": values[0],
                        "formation_domaine_libelle": strip_and_quote(values[1]),
                        "formation_niveau_libelle": strip_and_quote(values[2]),
                        "formation_commentaire": strip_and_quote(values[3]),
                        "formation_code_exigence": values[4],
                        "date_extraction": offre.get("dateExtraction"),
                    }
                )

                # pour "formation"
                if values not in seen_formation:
                    seen_formation.add(values)
                    formation.append(
                        {
                            "formation_code": values[0],
                            "formation_domaine_libelle": strip_and_quote(values[1]),
                            "formation_niveau_libelle": strip_and_quote(values[2]),
                            "formation_commentaire": strip_and_quote(values[3]),
                            "formation_code_exigence": values[4],
                        }
                    )

        #### pour "qualiteprofessionnelle" / "offre_qualiteprofessionnelle"
        qualitesprofessionnelles = offre.get("qualitesProfessionnelles")  # ⛔ Attention on a une liste de qualités professionnelles dans le json !!!

        if qualitesprofessionnelles:  # car on peut avoir dans le json "qualitesProfessionnelles": null
            for q in qualitesprofessionnelles:
                values = (
                    q.get("libelle"),
                    q.get("description"),
                )
                # pour "offre_qualiteprofessionnelle"
                offre_qualiteprofessionnelle.append(
                    {
                        "offre_id": offre_id,
                        "qualite_professionnelle_libelle": strip_and_quote(values[0]),
                        "qualite_professionnelle_description": strip_and_quote(values[1]),
                        "date_extraction": offre.get("dateExtraction"),
                    }
                )

                # pour "qualiteprofessionnelle"
                if values not in seen_qualiteprofessionnelle:
                    seen_qualiteprofessionnelle.add(values)
                    qualiteprofessionnelle.append(
                        {
                            "qualite_professionnelle_libelle": strip_and_quote(values[0]),
                            "qualite_professionnelle_description": strip_and_quote(values[1]),
                        }
                    )

        #### pour "qualification" / "offre_qualification"
        values = (
            offre.get("qualificationCode"),
            offre.get("qualificationLibelle"),
        )
        # pour "offre_qualification"
        offre_qualification.append(
            {
                "offre_id": offre_id,
                "qualification_code": values[0],
                "date_extraction": offre.get("dateExtraction"),
            }
        )

        # pour "qualification"
        if values not in seen_qualification:
            seen_qualification.add(values)
            qualification.append(
                {
                    "qualification_code": values[0],
                    "qualification_libelle": strip_and_quote(values[1]),
                }
            )

        #### pour "langue" / "offre_langue"
        langues = offre.get("langues")  # ⛔ Attention on a une liste de langues dans le json !!!

        if langues:
            for l in langues:
                values = (
                    l.get("libelle"),
                    l.get("exigence"),
                )

                # pour "offre_langue"
                offre_langue.append(
                    {
                        "offre_id": offre_id,
                        "langue_libelle": strip_and_quote(values[0]),
                        "langue_code_exigence": values[1],
                        "date_extraction": offre.get("dateExtraction"),
                    }
                )

                # pour "langue"
                if values not in seen_langue:
                    seen_langue.add(values)
                    langue.append(
                        {
                            "langue_libelle": strip_and_quote(values[0]),
                            "langue_code_exigence": values[1],
                        }
                    )

        #### pour "permisconduire" / "offre_permisconduire"
        permisconduires = offre.get("permis")  # ⛔ Attention on a une liste de permisconduires dans le json !!!

        if permisconduires:
            for pc in permisconduires:
                values = (
                    pc.get("libelle"),
                    pc.get("exigence"),
                )

                # pour "offre_permisconduire"
                offre_permisconduire.append(
                    {
                        "offre_id": offre_id,
                        "permis_libelle": strip_and_quote(values[0]),
                        "permis_code_exigence": values[1],
                        "date_extraction": offre.get("dateExtraction"),
                    }
                )

                # pour "permisconduire"
                if values not in seen_permisconduire:
                    seen_permisconduire.add(values)
                    permisconduire.append(
                        {
                            "permis_libelle": strip_and_quote(values[0]),
                            "permis_code_exigence": values[1],
                        }
                    )

    def write_json_file(folder, file, table_name):
        """Fonction simple pour DRY quelques lignes"""
        with open(os.path.join(folder, file), "w") as f:
            json.dump(table_name, f, ensure_ascii=False, indent=4)

    # Sauvegarde dans des "petits" fichiers json dédiés
    write_json_file(SPLIT_JSONS_DIR, "offreemploi.json", offreemploi)
    write_json_file(SPLIT_JSONS_DIR, "contrat.json", contrat)
    write_json_file(SPLIT_JSONS_DIR, "entreprise.json", entreprise)
    write_json_file(SPLIT_JSONS_DIR, "localisation.json", localisation)
    write_json_file(SPLIT_JSONS_DIR, "descriptionoffre.json", descriptionoffre)
    write_json_file(SPLIT_JSONS_DIR, "competence.json", competence)
    write_json_file(SPLIT_JSONS_DIR, "offre_competence.json", offre_competence)
    write_json_file(SPLIT_JSONS_DIR, "experience.json", experience)
    write_json_file(SPLIT_JSONS_DIR, "offre_experience.json", offre_experience)
    write_json_file(SPLIT_JSONS_DIR, "formation.json", formation)
    write_json_file(SPLIT_JSONS_DIR, "offre_formation.json", offre_formation)
    write_json_file(SPLIT_JSONS_DIR, "qualiteprofessionnelle.json", qualiteprofessionnelle)
    write_json_file(SPLIT_JSONS_DIR, "offre_qualiteprofessionnelle.json", offre_qualiteprofessionnelle)
    write_json_file(SPLIT_JSONS_DIR, "qualification.json", qualification)
    write_json_file(SPLIT_JSONS_DIR, "offre_qualification.json", offre_qualification)
    write_json_file(SPLIT_JSONS_DIR, "langue.json", langue)
    write_json_file(SPLIT_JSONS_DIR, "offre_langue.json", offre_langue)
    write_json_file(SPLIT_JSONS_DIR, "permisconduire.json", permisconduire)
    write_json_file(SPLIT_JSONS_DIR, "offre_permisconduire.json", offre_permisconduire)


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


def load_json(folder, filename):
    """
    Charge simplement le json
    Cette fonction ne peut pas être une task, car xcom n'est pas conçu pour stocker des objects volumineux.
    """
    with open(os.path.join(folder, filename), "r") as file:
        return json.load(file)


@task(task_id="OffreEmploi")
def insert_into_offreemploi(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table OffreEmploi"""

    offres = load_json(folder, json_filename)

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


@task(task_id="Contrat")
def insert_into_contrat(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Contrat"""

    offres = load_json(folder, json_filename)

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


@task(task_id="Entreprise")
def insert_into_entreprise(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Entreprise"""

    offres = load_json(folder, json_filename)

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


@task(task_id="Localisation")
def insert_into_localisation(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Localisation"""

    offres = load_json(folder, json_filename)

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
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation
                create_and_execute_insert_query(table_name="Localisation", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="DescriptionOffre")
def insert_into_description_offre(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table DescriptionOffre"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "offre_id": offre.get("offre_id"),
                    "intitule_offre": offre.get("intitule_offre"),
                    "description_offre": offre.get("description_offre"),
                    "nom_partenaire": offre.get("nom_partenaire"),
                    "rome_code": offre.get("rome_code"),
                    "rome_libelle": offre.get("rome_libelle"),
                    "appellation_rome": offre.get("appellation_rome"),
                    "difficile_a_pourvoir": offre.get("difficile_a_pourvoir"),
                    "accessible_travailleurs_handicapes": offre.get("accessible_travailleurs_handicapes"),
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation
                create_and_execute_insert_query(table_name="DescriptionOffre", row_data=values_dict, conflict_columns=["offre_id"], cursor=cursor)


@task(task_id="Competence")
def insert_into_competence(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Competence"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                competence_code = offre.get("competence_code")
                competence_libelle = offre.get("competence_libelle")
                competence_code_exigence = offre.get("competence_code_exigence")

                values_dict = {
                    "competence_code": competence_code,
                    "competence_libelle": competence_libelle,
                    "competence_code_exigence": competence_code_exigence,
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation
                create_and_execute_insert_query(table_name="Competence", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_Competence")
def insert_into_offre_competence(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_Competence"""
    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                competence_code = offre.get("competence_code")
                competence_libelle = offre.get("competence_libelle")
                competence_code_exigence = offre.get("competence_code_exigence")

                # requête pour récupérer competence_id
                query = """--sql
                            SELECT competence_id
                                FROM Competence
                            WHERE
                                competence_code = %s
                                AND competence_libelle = %s
                                AND competence_code_exigence = %s
                        """
                cursor.execute(query, (competence_code, competence_libelle, competence_code_exigence))

                result = cursor.fetchone()
                if result:
                    competence_id = result[0]
                else:
                    logging.error(f"Aucune correspondance pour : {competence_code} | {competence_libelle} | {competence_code_exigence}")
                    continue

                offre_id = offre.get("offre_id")
                date_extraction = offre.get("date_extraction")

                values_dict = {
                    "offre_id": offre_id,
                    "competence_id": competence_id,
                    "date_extraction": date_extraction,
                }

                create_and_execute_insert_query(table_name="Offre_Competence", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 competence_id différents :
            cursor.execute(f"""--sql
                               -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs competence_id
                               WITH latest_offre_id AS (
                                   SELECT DISTINCT ON (offre_id)
                                       offre_id,
                                       competence_id,
                                       date_extraction
                                   FROM Offre_Competence
                                   ORDER BY offre_id, date_extraction DESC
                               )
                               DELETE FROM Offre_Competence
                               WHERE (offre_id, competence_id, date_extraction) NOT IN (
                                   SELECT offre_id, competence_id, date_extraction
                                   FROM latest_offre_id
                               );
                            """)


@task(task_id="Experience")
def insert_into_experience(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Experience"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                experience_libelle = offre.get("experience_libelle")
                experience_code_exigence = offre.get("experience_code_exigence")
                experience_commentaire = offre.get("experience_commentaire")

                values_dict = {
                    "experience_libelle": experience_libelle,
                    "experience_code_exigence": experience_code_exigence,
                    "experience_commentaire": experience_commentaire,
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation
                create_and_execute_insert_query(table_name="Experience", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_Experience")
def insert_into_offre_experience(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_Experience"""
    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                experience_libelle = offre.get("experience_libelle")

                # requête pour récupérer experience_id
                if experience_libelle != None:  # parfois "experience_libelle" n'est pas renseigné
                    experience_code_exigence = offre.get("experience_code_exigence")
                    experience_commentaire = offre.get("experience_commentaire")

                    # print(experience_libelle, experience_code_exigence, experience_commentaire)  # pour investigation
                    if experience_commentaire is None:
                        query = """--sql
                                    SELECT experience_id
                                    FROM experience
                                    WHERE experience_libelle = %s
                                        AND experience_code_exigence = %s
                                        AND experience_commentaire IS NULL
                                """
                        cursor.execute(query, (experience_libelle, experience_code_exigence))
                    else:
                        query = """--sql
                                    SELECT experience_id
                                    FROM experience
                                    WHERE experience_libelle = %s
                                        AND experience_code_exigence = %s
                                        AND experience_commentaire = %s
                                """
                        cursor.execute(query, (experience_libelle, experience_code_exigence, experience_commentaire))

                    result = cursor.fetchone()
                    if result:
                        experience_id = result[0]
                    else:
                        logging.error(f"Aucune correspondance pour : {experience_libelle} | {experience_code_exigence} | {experience_commentaire}")
                        continue

                    offre_id = offre.get("offre_id")
                    date_extraction = offre.get("date_extraction")

                    values_dict = {
                        "offre_id": offre_id,
                        "experience_id": experience_id,
                        "date_extraction": date_extraction,
                    }

                    create_and_execute_insert_query(table_name="Offre_Experience", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 experience_id différents :
            cursor.execute(f"""--sql
                               -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs experience_id
                               WITH latest_offre_id AS (
                                   SELECT DISTINCT ON (offre_id)
                                       offre_id,
                                       experience_id,
                                       date_extraction
                                   FROM Offre_Experience
                                   ORDER BY offre_id, date_extraction DESC
                               )
                               DELETE FROM Offre_Experience
                               WHERE (offre_id, experience_id, date_extraction) NOT IN (
                                   SELECT offre_id, experience_id, date_extraction
                                   FROM latest_offre_id
                               );
                            """)


@task(task_id="Formation")
def insert_into_formation(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Formation"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                formation_domaine_libelle = offre.get("formation_domaine_libelle")
                formation_niveau_libelle = offre.get("formation_niveau_libelle")
                formation_commentaire = offre.get("formation_commentaire")
                formation_code_exigence = offre.get("formation_code_exigence")

                values_dict = {
                    "formation_code": offre.get("formation_code"),
                    "formation_domaine_libelle": formation_domaine_libelle,
                    "formation_niveau_libelle": formation_niveau_libelle,
                    "formation_commentaire": formation_commentaire,
                    "formation_code_exigence": formation_code_exigence,
                }

                # print(json.dumps(values_dict, indent=4, ensure_ascii=False))  # print pour investigation
                create_and_execute_insert_query(table_name="Formation", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_Formation")
def insert_into_offre_formation(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_Formation"""
    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                formation_domaine_libelle = offre.get("formation_domaine_libelle")
                formation_niveau_libelle = offre.get("formation_niveau_libelle")
                formation_commentaire = offre.get("formation_commentaire")

                if all([formation_domaine_libelle, formation_niveau_libelle, formation_commentaire]):
                    formation_code = offre.get("formation_code")
                    formation_code_exigence = offre.get("formation_code_exigence")

                    # requête pour récupérer formation_id
                    query = """--sql
                                SELECT formation_id
                                FROM Formation
                                WHERE
                                    formation_code = %s
                                    AND formation_domaine_libelle = %s
                                    AND formation_niveau_libelle = %s
                                    AND formation_commentaire = %s
                                    AND formation_code_exigence = %s
                            """

                    cursor.execute(query, (formation_code, formation_domaine_libelle, formation_niveau_libelle, formation_commentaire, formation_code_exigence))

                    result = cursor.fetchone()
                    if result:
                        formation_id = result[0]
                    else:
                        logging.error(f"Aucune correspondance pour : {formation_code} | {formation_domaine_libelle} | {formation_niveau_libelle} | {formation_commentaire} | {formation_code_exigence}")
                        continue

                    offre_id = offre.get("offre_id")
                    date_extraction = offre.get("date_extraction")

                    values_dict = {
                        "offre_id": offre_id,
                        "formation_id": formation_id,
                        "date_extraction": date_extraction,
                    }

                    create_and_execute_insert_query(table_name="Offre_Formation", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 formation_id différents :
            cursor.execute(f"""--sql
                               -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs formation_id
                               WITH latest_offre_id AS (
                                   SELECT DISTINCT ON (offre_id)
                                       offre_id,
                                       formation_id,
                                       date_extraction
                                   FROM Offre_Formation
                                   ORDER BY offre_id, date_extraction DESC
                               )
                               DELETE FROM Offre_Formation
                               WHERE (offre_id, formation_id, date_extraction) NOT IN (
                                   SELECT offre_id, formation_id, date_extraction
                                   FROM latest_offre_id
                               );
                               """)


@task(task_id="QualiteProfessionnelle")
def insert_into_qualiteprofessionnelle(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table QualiteProfessionnelle"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "qualite_professionnelle_libelle": offre.get("qualite_professionnelle_libelle"),
                    "qualite_professionnelle_description": offre.get("qualite_professionnelle_description"),
                }

                create_and_execute_insert_query(table_name="QualiteProfessionnelle", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_QualiteProfessionnelle")
def insert_into_offre_qualiteprofessionnelle(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_QualiteProfessionnelle"""
    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                qualite_professionnelle_libelle = offre.get("qualite_professionnelle_libelle")
                qualite_professionnelle_description = offre.get("qualite_professionnelle_description")

                # requête pour récupérer qualite_professionnelle_id
                query = """--sql
                            SELECT qualite_professionnelle_id
                            FROM QualiteProfessionnelle
                            WHERE
                                qualite_professionnelle_libelle = %s
                                AND qualite_professionnelle_description = %s
                        """

                cursor.execute(query, (qualite_professionnelle_libelle, qualite_professionnelle_description))

                result = cursor.fetchone()
                if result:
                    qualite_professionnelle_id = result[0]
                else:
                    logging.error(f"Aucune correspondance pour : {qualite_professionnelle_libelle} | {qualite_professionnelle_description}")
                    continue

                offre_id = offre.get("offre_id")
                date_extraction = offre.get("date_extraction")

                values_dict = {
                    "offre_id": offre_id,
                    "qualite_professionnelle_id": qualite_professionnelle_id,
                    "date_extraction": date_extraction,
                }

                create_and_execute_insert_query(table_name="Offre_QualiteProfessionnelle", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 qualite_professionnelle_id différents :
            cursor.execute(f"""--sql
                               -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs qualite_professionnelle_id
                               WITH latest_offre_id AS (
                                   SELECT DISTINCT ON (offre_id)
                                       offre_id,
                                       qualite_professionnelle_id,
                                       date_extraction
                                   FROM Offre_QualiteProfessionnelle
                                   ORDER BY offre_id, date_extraction DESC
                               )
                               DELETE FROM Offre_QualiteProfessionnelle
                               WHERE (offre_id, qualite_professionnelle_id, date_extraction) NOT IN (
                                   SELECT offre_id, qualite_professionnelle_id, date_extraction
                                   FROM latest_offre_id
                               );
                            """)


@task(task_id="Qualification")
def insert_into_qualification(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Qualification"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                qualification_code = offre.get("qualification_code")
                qualification_libelle = offre.get("qualification_libelle")
                values_dict = {
                    "qualification_code": qualification_code,
                    "qualification_libelle": qualification_libelle,
                }

                if (qualification_code is not None) or (qualification_libelle is not None):
                    create_and_execute_insert_query(table_name="Qualification", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_Qualification")
def insert_into_offre_qualification(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_Qualification"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                offre_id = offre.get("offre_id")
                qualification_code = offre.get("qualification_code")
                date_extraction = offre.get("date_extraction")

                values_dict = {
                    "offre_id": offre_id,
                    "qualification_code": qualification_code,
                    "date_extraction": date_extraction,
                }

                if qualification_code:
                    create_and_execute_insert_query(table_name="Offre_Qualification", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 qualification_code différents :
            cursor.execute(f"""--sql
                                -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs qualification_code
                                WITH latest_offre_id AS (
                                    SELECT DISTINCT ON (offre_id)
                                        offre_id,
                                        qualification_code,
                                        date_extraction
                                    FROM offre_qualification
                                    ORDER BY offre_id, date_extraction DESC
                                )
                                DELETE FROM offre_qualification
                                WHERE (offre_id, qualification_code, date_extraction) NOT IN (
                                    SELECT offre_id, qualification_code, date_extraction
                                    FROM latest_offre_id
                                );
                            """)


@task(task_id="Langue")
def insert_into_langue(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Langue"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "langue_libelle": offre.get("langue_libelle"),
                    "langue_code_exigence": offre.get("langue_code_exigence"),
                }

                create_and_execute_insert_query(table_name="Langue", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_Langue")
def insert_into_offre_langue(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_Langue"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                langue_libelle = offre.get("langue_libelle")
                langue_code_exigence = offre.get("langue_code_exigence")

                # requête pour récupérer langue_id
                query = """--sql
                            SELECT langue_id
                            FROM Langue
                            WHERE langue_libelle = %s
                              AND langue_code_exigence = %s
                        """
                cursor.execute(query, (langue_libelle, langue_code_exigence))

                result = cursor.fetchone()
                if result:
                    langue_id = result[0]
                else:
                    logging.error(f"Aucune correspondance pour : {langue_libelle} | {langue_code_exigence}")
                    continue

                offre_id = offre.get("offre_id")
                date_extraction = offre.get("date_extraction")

                values_dict = {
                    "offre_id": offre_id,
                    "langue_id": langue_id,
                    "date_extraction": date_extraction,
                }

                create_and_execute_insert_query(table_name="Offre_Langue", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 langue_id différents :
            cursor.execute(f"""--sql
                        -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs langue_id
                        WITH latest_offre_id AS (
                            SELECT DISTINCT ON (offre_id)
                                offre_id,
                                langue_id,
                                date_extraction
                            FROM Offre_Langue
                            ORDER BY offre_id, date_extraction DESC
                        )
                        DELETE FROM Offre_Langue
                        WHERE (offre_id, langue_id, date_extraction) NOT IN (
                            SELECT offre_id, langue_id, date_extraction
                            FROM latest_offre_id
                        );
                        """)


@task(task_id="PermisConduire")
def insert_into_permisconduire(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Permis_Conduire"""

    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                values_dict = {
                    "permis_libelle": offre.get("permis_libelle"),
                    "permis_code_exigence": offre.get("permis_code_exigence"),
                }

                create_and_execute_insert_query(table_name="PermisConduire", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)


@task(task_id="Offre_PermisConduire")
def insert_into_offre_permisconduire(folder, json_filename):
    """Récupération des valeurs depuis le "json_filename" et écriture en base de données dans la table Offre_PermisConduire"""
    offres = load_json(folder, json_filename)

    with psycopg2.connect(**DB_PARAM) as conn:
        with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
            for offre in offres:
                permis_libelle = offre.get("permis_libelle")
                permis_code_exigence = offre.get("permis_code_exigence")

                # requête pour récupérer permis_id
                query = """--sql
                            SELECT permis_id
                            FROM permisconduire
                            WHERE permis_libelle = %s
                            AND permis_code_exigence = %s
                        """
                cursor.execute(query, (permis_libelle, permis_code_exigence))

                result = cursor.fetchone()
                if result:
                    permis_id = result[0]
                else:
                    logging.error(f"Aucune correspondance pour : {permis_libelle} | {permis_code_exigence}")
                    continue

                offre_id = offre.get("offre_id")
                date_extraction = offre.get("date_extraction")

                values_dict = {
                    "offre_id": offre_id,
                    "permis_id": permis_id,
                    "date_extraction": date_extraction,
                }

                create_and_execute_insert_query(table_name="Offre_PermisConduire", row_data=values_dict, conflict_columns=values_dict.keys(), cursor=cursor)

            # On supprime les lignes où 1 offre_id est présente avec 2 permis_id différents :
            cursor.execute(f"""--sql
                        -- CTE pour afficher l'offre_id le plus récent s'il y a 1 offre_id avec plusieurs permis_id
                        WITH latest_offre_id AS (
                            SELECT DISTINCT ON (offre_id)
                                offre_id,
                                permis_id,
                                date_extraction
                            FROM Offre_PermisConduire
                            ORDER BY offre_id, date_extraction DESC
                        )
                        DELETE FROM Offre_PermisConduire
                        WHERE (offre_id, permis_id, date_extraction) NOT IN (
                            SELECT offre_id, permis_id, date_extraction
                            FROM latest_offre_id
                        );
                        """)


keep_generated_split_jsons = 1  # (mode dev) False pour ne pas supprimer les jsons splittés générés

# définition de paramètres liés au mécanisme de retry pour une tâche
default_args = {
    "retries": 5,  # nombre de tentatives de ré-exécution en cas d’échec d’une tâche
    "retry_delay": timedelta(minutes=1),  # délai entre deux tentatives de retry (après un échec)
    "retry_exponential_backoff": True,  # si True : le délai entre les retries augmente de façon exponentielle (ex: 2 min → 4 min → 8 min → ...)
    "max_retry_delay": timedelta(minutes=5),  # délai maximum entre deux retries, même si activation de backoff exponentiel
}


with DAG(
    dag_id="DAG_2_WRITE_TO_DATABASE",
    tags=["project"],
    default_args=default_args,
):
    with TaskGroup(group_id="SETUP") as setup:
        json_file_path = check_only_one_json_file_in_folder(AGGREGATED_JSON_DIR)

        if keep_generated_split_jsons:
            remove = remove_all_split_jsons(SPLIT_JSONS_DIR)

        create_tables = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="create_all_tables_if_not_existing",
            sql=os.path.join("sql", "create_all_tables.sql"),
        )

        postgres = ensure_postgres_connexion(conn_id)

        if keep_generated_split_jsons:
            split_json = split_large_json(json_file_path)

            json_file_path >> postgres >> create_tables
            json_file_path >> remove >> split_json

    with TaskGroup(group_id="INSERT_INTO_TABLES_WITHOUT_JUNCTION") as without_junction:
        """ "INSERT INTO" pour les tables qui n'ont pas de tables de liaison """
        insert_into_offreemploi(SPLIT_JSONS_DIR, "offreemploi.json")
        insert_into_contrat(SPLIT_JSONS_DIR, "contrat.json")
        insert_into_entreprise(SPLIT_JSONS_DIR, "entreprise.json")
        insert_into_localisation(SPLIT_JSONS_DIR, "localisation.json")
        insert_into_description_offre(SPLIT_JSONS_DIR, "descriptionoffre.json")

    with TaskGroup(group_id="INSERT_INTO_TABLES_WITH_JUNCTION", tooltip="xxx") as with_junction:
        """ "INSERT INTO" pour les tables qui ont un lieu avec une table de liaison : tables de dimension d'abord, tables de liaison après """
        i1 = insert_into_competence(SPLIT_JSONS_DIR, "competence.json")
        i2 = insert_into_experience(SPLIT_JSONS_DIR, "experience.json")
        i3 = insert_into_formation(SPLIT_JSONS_DIR, "formation.json")
        i4 = insert_into_qualiteprofessionnelle(SPLIT_JSONS_DIR, "qualiteprofessionnelle.json")
        i5 = insert_into_qualification(SPLIT_JSONS_DIR, "qualification.json")
        i6 = insert_into_langue(SPLIT_JSONS_DIR, "langue.json")
        i7 = insert_into_permisconduire(SPLIT_JSONS_DIR, "permisconduire.json")

        j1 = insert_into_offre_competence(SPLIT_JSONS_DIR, "offre_competence.json")
        j2 = insert_into_offre_experience(SPLIT_JSONS_DIR, "offre_experience.json")
        j3 = insert_into_offre_formation(SPLIT_JSONS_DIR, "offre_formation.json")
        j4 = insert_into_offre_qualiteprofessionnelle(SPLIT_JSONS_DIR, "offre_qualiteprofessionnelle.json")
        j5 = insert_into_offre_qualification(SPLIT_JSONS_DIR, "offre_qualification.json")
        j6 = insert_into_offre_langue(SPLIT_JSONS_DIR, "offre_langue.json")
        j7 = insert_into_offre_permisconduire(SPLIT_JSONS_DIR, "offre_permisconduire.json")

        i1 >> j1
        i2 >> j2
        i3 >> j3
        i4 >> j4
        i5 >> j5
        i6 >> j6
        i7 >> j7

    with TaskGroup(group_id="TRANSFORMATIONS") as transformations:
        """
        Deuxième set de transformations par requête SQL
        (le premier set de transformations étant fait côté Python dans le DAG 1)
        """

        t1 = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="update_descriptionoffre_metier_data_DE",
            sql=os.path.join("sql", "transformation_1_update__table_descriptionoffre__column__metier_data__DE.sql"),
        )

        t2 = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="update_descriptionoffre_metier_data_DA",
            sql=os.path.join("sql", "transformation_2_update__table_descriptionoffre__column__metier_data__DA.sql"),
        )

        t3 = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="update_descriptionoffre_metier_data_DS",
            sql=os.path.join("sql", "transformation_3_update__table_descriptionoffre__column__metier_data__DS.sql"),
        )

        t4 = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="update_contrat_salaires_min_max",
            sql=os.path.join("sql", "transformation_4_update__table_contrat__columns__salaire_min__salaire_max.sql"),
        )

        t5 = SQLExecuteQueryOperator(
            conn_id=conn_id,
            task_id="update_descriptionoffre_column_liste_mots_cles",
            sql=os.path.join("sql", "transformation_5_update__table_descriptionoffre__column__liste_mots_cles.sql"),
        )

        [t1, t2, t3, t4] >> t5

    setup >> without_junction >> with_junction >> transformations
