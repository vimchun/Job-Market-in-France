import os

from datetime import datetime

import yaml


# from colorama import init
from functions import concatenate_all_json_into_one, get_bearer_token, get_offres, get_referentiel_appellations_rome, get_referentiel_pays, keep_only_offres_from_metropole, remove_all_json_files

# init(autoreset=True)  # pour colorama, inutile de reset si on colorie

# Récupération des credentials données sur le site de FT, depuis un fichier yaml
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script
current_directory = os.path.dirname(os.path.abspath(__file__))
credential_filename = os.path.join(current_directory, CREDENTIALS_FILE)
json_files_directory = os.path.join(current_directory, "outputs", "offres")

with open(credential_filename, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)


# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
#  note : il faut tout mettre à 1 pour le script de bout en bout
launch_get_referentiel_appellations_rome = 0
launch_get_referentiel_pays = 0
launch_remove_all_json_files = 0
launch_get_offres = 0
launch_concatenate_all_json_into_one = 1
launch_keep_only_offres_from_metropole = 1

if launch_get_referentiel_appellations_rome:
    get_referentiel_appellations_rome(token)

#################################################################################################################################

if launch_get_referentiel_pays:
    get_referentiel_pays(token)

#################################################################################################################################

if launch_remove_all_json_files:
    remove_all_json_files(json_files_directory)

#################################################################################################################################

if launch_get_offres:
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
    today = datetime.now()
    date_now = today.strftime("%Y-%m-%d--%Hh%M")
    concatenated_json_filename = f"_offres_concatenated.json"
    concatenated_json_filename_path = os.path.join(json_files_directory, concatenated_json_filename)

    df_concat = concatenate_all_json_into_one(json_files_directory, concatenated_json_filename)

    # On renomme le fichier avec le nombre d'offres et la date/heure au lancement de la fonction
    json_final_name = f"{concatenated_json_filename[:-5]}_{df_concat.shape[0]}_offres__{date_now}.json"

    os.rename(
        concatenated_json_filename_path,
        os.path.join(json_files_directory, json_final_name),
    )


if launch_keep_only_offres_from_metropole:
    # json_final_name = "_offres_concatenated_13639_offres__2025-03-02--23h46.json"  # à décommenter si besoin de hardcoder
    keep_only_offres_from_metropole(json_files_directory, json_final_name)
