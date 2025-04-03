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
if len(json_file_in_generated_directory) == 1:  # en premier car cas le plus fréquent
    # Le dossier contient 1 fichier json.
    current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_0.json

    # On renomme le fichier json en mettant à jour la date et l'heure et on incrémente le numéro de l'occurence dans le nom du fichier

    occurence_number = int(Path(current_json_file).stem.split("extraction_occurence_")[1])  # note : stem pour récupérer le nom du fichier sans l'extension
    occurence_number += 1

    json_filename = f"{today}__extraction_occurence_{occurence_number}.json"

    print(
        f'Il y a 1 fichier json ("{current_json_file}") dans le dossier "{generated_json_files_directory}"',
        "",
        f"{Fore.RED}== Lancement de l'extraction occurence {occurence_number} ==",
        f'Nouveau nom fichier json : "{json_filename}"',
        sep="\n",
    )

    # archive de l'ancien fichier avant de le renommer et de le traiter
    # shutil.copy(
    #     os.path.join(generated_json_files_directory, current_json_file),
    #     os.path.join(generated_json_files_directory, "archive_json_files", current_json_file),
    # )

    os.rename(
        os.path.join(generated_json_files_directory, current_json_file),
        os.path.join(generated_json_files_directory, json_filename),
    )

    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)

    print(df)


elif not json_file_in_generated_directory:
    # Le dossier contient 0 fichier json.
    print(
        f'Il n\'y a pas de fichier json dans le dossier "{generated_json_files_directory}"',
        f"{Fore.RED}== Lancement de l'extraction occurence 1 ==",
        sep="\n",
    )

    json_filename = f"{today}__extraction_occurence_1.json"

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
launch_remove_all_get_json_files = 1  # ~ quelques secondes
launch_get_offres = 1  # ~ 20 minutes
launch_concatenate_all_json_into_one = 1  # ~ 1 minute
launch_add_date_extract_attribute = 1  # ~ quelques secondes
launch_keep_only_offres_from_metropole = 1  # ~ quelques secondes
launch_add_location_attributes = 1  # ~ 5 minutes
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

#################################################################################################################################

if launch_get_referentiel_pays:
    get_referentiel_pays(token)

#################################################################################################################################

if launch_remove_all_get_json_files:
    remove_all_json_files(json_files_original_from_api_directory)

#################################################################################################################################

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
        get_offres(
            token,
            code_appellation_libelle,
            filter_params={
                #### table DescriptionOffre
                "appellation": code,  # Code appellation ROME de l’offre
                # "theme": "",  # Thème ROME du métier
                # "accesTravailleurHandicape": True,  # Offres pour lesquelles l’employeur est handi friendly
                # "origineOffre": "",  # Origine de l'offre
                # "partenaires": "",  # Chaine de caractères - Liste des codes partenaires dont les offres sont à inclure ou exclure en fonction du mode de sélection associé et du filtre de l’origine de l’offre # noqa
                # "offresManqueCandidats": "",  # Filtre sur les offres difficiles à pouvoir
                # "codeROME": "",  # Code ROME de l’offre, voir le référentiel des métiers ci-dessous
                # "domaine": "",  # Domaine de l’offre
                #### table OffreEmploi
                # date de création (ne permet de pas récupérer les offres anciennes)
                # "minCreationDate": "2015-01-01T00:00:00Z",  # Date minimale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "maxCreationDate": "2025-01-12T00:00:00Z",  # Date maximale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "publieeDepuis": "31",  # Recherche les offres publiées depuis maximum « X » jours (1, 3, 7, 14 ou 31 attendu.)
                #### table Contrat
                # "dureeContratMax": "",  # Recherche les offres avec une durée de contrat maximale (format double de 0 à 99 bornes incluses)
                # "dureeContratMin": "",  # Recherche les offres avec une durée de contrat minimale (format double de 0 à 99 bornes incluses)
                # "dureeHebdo": "",  # Type de durée du contrat de l'offre
                # "dureeHebdoMax": "",  # Recherche les offres avec une durée maximale (format HHMM)
                # "dureeHebdoMin": "",  # Recherche les offres avec une durée minimale (format HHMM)
                # "tempsPlein": "",  # Temps plein ou partiel
                # "natureContrat": "",  # Code de la nature du contrat
                # "typeContrat": "",  # Code du type de contrat
                # "periodeSalaire": "",  # Période pour le calcul du salaire minimum (M Mensuel, A Annuel, H Horaire, C Cachet). Si cette donnée est renseignée, le salaire minimum est obligatoire. # noqa
                # "salaireMin": "",  # Salaire minimum recherché. Si cette donnée est renseignée, le code du type de salaire minimum est obligatoire.
                #### table Entreprise
                # "modeSelectionPartenaires": "",  # Énumération (INCLUS ou EXCLU) - Mode de sélection des partenaires.
                # "codeNAF": "",  # Code NAF de l’offre, (format 99.99X)
                # "secteurActivite": "",  # Division NAF de l’offre (2 premiers chiffres)
                # "entreprisesAdaptees": "",  # Filtre sur les offres dont les entreprises sont adaptées
                #### table Localisation
                "paysContinent": "01",  # Pays ou continent de l’offre, 01 pour la France (non restreint à la métropôle)
                # "paysContinent": "02",  # pour l'Allemagne (presque pas d'offre)
                # "paysContinent": "04",  # pour la Belgique (presque pas d'offre)
                # "commune": "",  # Code INSEE de la commune
                # "departement": "",  # Département de l’offre (Jusqu'à 5 valeurs possibles, séparées par une virgule)
                # "distance": "",  # Distance à la commune (pris en compte uniquement si une commune est renseignée
                # "inclureLimitrophes": "",  # Inclure les départements limitrophes dans la recherche
                # "region": "",  # Région de l’offre
                #### table Experience
                # "experience": "",  # Niveau d’expérience demandé, (1 moins d'un an, 2 de 1 à 3 ans, 3 plus de 3 ans)
                # "experienceExigence": "D",  # Exigence d'expérience (D débutant accepté, S expérience souhaitée, E expérience exigée)
                #### table Formation
                # "niveauFormation": "",  # Niveau de formation demandé
                #### table Qualification
                # "qualification": "",  # Qualification du poste (0 non-cadre, 9 cadre)
                #### table PermisConduire
                # "permis": "",  # Permis demandé
                #### misc.
                # "sort": "",  # Tri selon 3 façons différentes
                # "motsCles": "data",  # Recherche de mots clés dans l’offre  # note: on n'utilise pas ce paramètre pour avoir le plus d'offres possible
                # "offresMRS": "",  # Uniquement les offres d'emplois avec méthode de recrutement par simulation proposée
            },
        )

    # Notes :
    # Pour filtrer qu'en France métropolitaine :
    #   - On ne peut pas filtrer sur les 13 régions en une fois (une seule région possible dans la requête)
    #   - On ne peut mettre que 5 départements d'un coup

#################################################################################################################################

if launch_concatenate_all_json_into_one:
    concatenate_all_json_into_one(
        json_files_from_api_directory=json_files_original_from_api_directory,
        generated_json_file_directory=generated_json_files_directory,
        new_json_filename=json_filename,  # on écrase le fichier en entrée
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))

#################################################################################################################################

if launch_add_date_extract_attribute:
    add_date_extract_attribute(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename,
        new_json_filename=json_filename,  # on écrase le fichier en entrée
        # date_to_insert="2025-03-22",  # à commenter si on veut mettre la date du jour
        # la valeur "date_to_insert" écrase la valeur si l'attribut est existant dans le json
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)
    print(f'{Fore.YELLOW}{df.shape}   -   Valeur de "dateExtraction" pour le premier document json : {df.loc[1, "dateExtraction"]}')

#################################################################################################################################

if launch_keep_only_offres_from_metropole:
    keep_only_offres_from_metropole(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename,
        new_json_filename=json_filename,  # on écrase le fichier en entrée
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))

#################################################################################################################################

if launch_add_location_attributes:
    add_location_attributes(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename,
        new_json_filename=json_filename,
    )

    # Print de la shape du DataFrame du json nouvellement écrit pour information
    print(Fore.YELLOW + str(pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False).shape))
