import csv
import os
import shutil
import sys

from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

from colorama import Fore, Style, init

init(autoreset=True)  # pour colorama, inutile de reset si on colorie

from functions import (
    add_date_ecriture_offre_attribute,
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

#### "Partie paramétrable"
# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
#  => Il faut mettre à 1 toutes les variables suivantes pour exécuter le script de bout en bout.
launch_remove_all_get_json_files = 1  # ~ quelques secondes
launch_get_offres = 1  # ~ 20 minutes
launch_concatenate_all_json_into_one = 1  # ~ 1 minute
#
launch_add_date_extract_attribute = 1  # ~ quelques secondes
launch_add_date_ecriture_offre_attribute = 1
launch_keep_only_offres_from_metropole = 1  # ~ quelques secondes
launch_add_location_attributes = 1  # ~ 5 minutes
#### Fin "Partie paramétrable"


# Récupération des credentials données sur le site de FT, depuis un fichier yaml
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script
current_directory = os.path.dirname(os.path.abspath(__file__))
#
generated_json_files_directory = os.path.join(current_directory, "outputs", "offres", "1--generated_json_file")
#
credential_filename = os.path.join(current_directory, CREDENTIALS_FILE)
codes_appellation_filename = os.path.join(current_directory, "code_appellation_libelle.yml")
json_files_original_from_api_directory = os.path.join(current_directory, "outputs", "offres", "0--original_json_files_from_api")

with open(credential_filename, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)


def functions_sequence(json_files_from_api_directory, generated_json_files_directory, json_filename):
    """
    Cette fonction exécute les fonctions suivantes à exécuter séquentiellement :
        - remove_all_json_files()
        - get_offres()
        - concatenate_all_json_into_one()
        - keep_only_offres_from_metropole()
        - add_location_attributes()
        - add_date_extract_attribute()

    si les booléens associés respectifs sont activées :
        - launch_remove_all_get_json_files
        - launch_concatenate_all_json_into_one
        - launch_keep_only_offres_from_metropole
        - launch_add_location_attributes
        - launch_add_date_extract_attribute
    """

    if launch_remove_all_get_json_files:
        remove_all_json_files(json_files_original_from_api_directory)
    ####
    if launch_get_offres:
        print(f'{Fore.GREEN}\n==> Fonction "get_offres()"\n')

        with open(codes_appellation_filename, "r") as file:
            content = yaml.safe_load(file)
            code_appellation_libelle = content["code_appellation_libelle"]
            codes_list = [i["code"] for i in code_appellation_libelle]

        for code in codes_list:
            get_offres(token, code_appellation_libelle, filter_params={"appellation": code, "paysContinent": "01"})
            # Note : "paysContinent": "01" pour la France (non restreint à la métropôle)
    ####
    if launch_concatenate_all_json_into_one:
        concatenate_all_json_into_one(
            json_files_from_api_directory=json_files_from_api_directory,
            generated_json_file_directory=generated_json_files_directory,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
        )
        print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
    ####
    if launch_keep_only_offres_from_metropole:
        keep_only_offres_from_metropole(
            json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
        )
        print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
    ####
    if launch_add_location_attributes:
        add_location_attributes(
            json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
        )
        print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))  # Print shape df du json nouvellement écrit
    ####
    if launch_add_date_extract_attribute:
        add_date_extract_attribute(
            json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
            date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
            # date_to_insert="2025-04-05",  # à commenter si on veut mettre la date du jour
            # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
        )
        df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)
        print(f'{Fore.YELLOW}{df.shape}   -   Valeur de "dateExtraction" pour le premier document json : {df.loc[1, "dateExtraction"]}')  # Print shape df du json nouvellement écrit


if 1:
    # création liste avec tous les fichiers json
    json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]

    now = datetime.now().strftime("%Y-%m-%d--%Hh%M")

    # Le script continue si le dossier "1--generated_json_file" contient 0 ou 1 fichier json

    if len(json_file_in_generated_directory) == 1:  # en premier car cas le plus fréquent
        #### Le dossier contient 1 fichier json.
        current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_1.json

        # Création d'un nouveau json, créé à partir des nouvelles offres, avec de nouveaux appels API
        occurence_number = int(Path(current_json_file).stem.split("extraction_occurence_")[1])  # note : stem pour récupérer le nom du fichier sans l'extension
        new_json_file = f"{now}__extraction_occurence_{occurence_number+1}.json"

        print(
            f'Il y a 1 fichier json dans le dossier "{generated_json_files_directory}"',
            f' -> json_1 = "{Fore.YELLOW}{current_json_file}{Style.RESET_ALL}"',
            "",
            f"{Fore.RED}== Lancement de l'extraction occurence {occurence_number+1} ==",
            f'On va créer json_2 = "{Fore.YELLOW}{new_json_file}{Style.RESET_ALL}" à partir de nouvelles requêtes API, qui après traitement sera le seul json qui restera dans le dossier',
            sep="\n",
        )

        functions_sequence(
            json_files_from_api_directory=json_files_original_from_api_directory,
            generated_json_files_directory=generated_json_files_directory,
            json_filename=new_json_file,
        )

        print("\nConcaténation entre le json précédemment présent dans le dossier, et le json nouvellement créé\n")
        df1 = pd.read_json(os.path.join(generated_json_files_directory, current_json_file), dtype=False)
        df2 = pd.read_json(os.path.join(generated_json_files_directory, new_json_file), dtype=False)

        #
        intersection_ids = pd.merge(df1, df2, on="id")["id"].tolist()
        df1_minus_intersection = df1[~df1.id.isin(intersection_ids)]  # c'est la "partie_1" dans "workflow_db_update.drawio"
        df_concat = pd.concat([df1_minus_intersection, df2])  # concaténation de "partie_1" et "partie_2" (cf "workflow_db_update.drawio")

        # Ecriture du nom du fichier et du nombre d'offres dans le fichier "_json_files_history.csv"
        with open(os.path.join(generated_json_files_directory, "_json_files_history.csv"), "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([new_json_file, len(df_concat)])

        # Ecriture dans le fichier json
        df_concat.to_json(
            os.path.join(generated_json_files_directory, new_json_file),
            orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
            force_ascii=False,  # pour convertir les caractères spéciaux
            indent=4,  # pour formatter la sortie
        )

        # On supprime les backslashs ajoutés par la méthode .to_json()
        with open(os.path.join(generated_json_files_directory, new_json_file), "r", encoding="utf-8") as f:
            content = f.read()

            content = content.replace("\\/", "/")  # On remplace "\/" par "/"
            content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

            # On sauvegarde le fichier final sans les '\'
            with open(os.path.join(generated_json_files_directory, new_json_file), "w", encoding="utf-8") as f:
                f.write(content)

        ####
        if launch_add_date_ecriture_offre_attribute:
            add_date_ecriture_offre_attribute(
                json_files_directory=generated_json_files_directory,
                json_filename=new_json_file,
                new_json_filename=new_json_file,  # on écrase le fichier en entrée
                # date_to_insert="2025-04-10",  # à commenter si on veut mettre la date du jour
                # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
                overwrite_all_lines=False,
            )

        # ####
        # if launch_add_date_ecriture_offre_attribute:
        #     add_date_ecriture_offre_attribute(
        #         json_files_directory=generated_json_files_directory,
        #         json_filename=json_filename,
        #         new_json_filename=json_filename,  # on écrase le fichier en entrée
        #         # date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
        #         date_to_insert="2025-04-05",  # à commenter si on veut mettre la date du jour
        #         # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
        #         overwrite_all_lines=False,
        #     )

        print(f"{Fore.YELLOW}Shape du df du json concaténé : {pd.read_json(os.path.join(generated_json_files_directory, new_json_file), dtype=False).shape}")

        # Le nouveau json a été mis à jour avec la concaténation, il reste à déplacer l'ancien fichier json dans le dossier "archive_json_files"
        shutil.move(
            os.path.join(generated_json_files_directory, current_json_file),
            os.path.join(generated_json_files_directory, "archive_json_files", current_json_file),
        )

        ####

    elif not json_file_in_generated_directory:
        #### Le dossier contient 0 fichier json.
        print(
            f'Il n\'y a pas de fichier json dans le dossier "{generated_json_files_directory}"',
            f"{Fore.RED}== Lancement de l'extraction occurence 1 ==",
            sep="\n",
        )

        json_filename = f"{now}__extraction_occurence_1.json"

        functions_sequence(
            json_files_from_api_directory=json_files_original_from_api_directory,
            generated_json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
        )

        # todo : à revoir/tester ce qui suit
        # if launch_add_date_ecriture_offre_attribute:  #
        #     add_date_ecriture_offre_attribute(
        #         json_files_directory=generated_json_files_directory,
        #         json_filename=new_json_file,
        #         new_json_filename=new_json_file,  # on écrase le fichier en entrée
        #         # date_to_insert="2025-04-05",  # à commenter si on veut mettre la date du jour
        #         # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
        #         overwrite_all_lines=False,
        #     )

        ####

    elif len(json_file_in_generated_directory) > 1:
        #### Il y a plus d'un fichier, on arrête le script car le dossier doit en contenir 0 ou 1.
        print(
            f'Il y a plusieurs fichiers json dans le dossier : "{generated_json_files_directory}" (il n\'en faut que 0 ou 1)',
            f"{Fore.RED}== Arrêt du script ==",
            sep="\n",
        )
        sys.exit()


####
if 0:
    """
    Ce qui suit n'a normalement pas besoin d'être lancé car les fonctions ont déjà générés les fichiers (voir commentaires)
    On laisse cette partie au cas où ça pourrait servir, par exemple pour mettre à jour un des fichiers.
    """
    launch_get_referentiel_appellations_rome = 0  # fichier "appellations_rome.json" déjà généré et poussé
    launch_get_referentiel_pays = 0  # fichier "pays.json" déjà généré et poussé
    launch_create_location_csv = 1  # fichier "code_name__city_department_region.csv" déjà généré et poussé

    if launch_get_referentiel_appellations_rome:
        get_referentiel_appellations_rome(token)

    if launch_get_referentiel_pays:
        get_referentiel_pays(token)

    if launch_create_location_csv:
        create_csv__code_name__city_department_region()

####
if 0:
    """
    Bloc de test, par exemple pour ajouter des attributs à un json
    """

    if 1:
        """
        Prendre un json, et modifier ses attributs "dateExtraction" et "dateEcritureOffre"
        """

        json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]
        json_filename = json_file_in_generated_directory[0]

        # print(
        #     generated_json_files_directory,
        #     json_file_in_generated_directory[0],
        # )
        df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

        add_date_extract_attribute(
            json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
            date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
        )

        print(
            # df.dateExtraction,
            # df.dateEcritureOffre,
            # sep="\n\n",
        )

        add_date_ecriture_offre_attribute(
            json_files_directory=generated_json_files_directory,
            json_filename=json_filename,
            new_json_filename=json_filename,  # on écrase le fichier en entrée
            date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
            overwrite_all_lines=False,
        )

        df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

        print(
            # df.dateExtraction,
            df.dateEcritureOffre,
            sep="\n\n",
        )
