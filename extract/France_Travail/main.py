import os

import yaml

from colorama import Fore, init

from functions import merge_all_json_into_one, get_bearer_token, get_offres, get_referentiel_appellations_rome, get_referentiel_pays

init(autoreset=True)  # pour colorama, inutile de reset si on colorie


# Récupération des credentials données sur le site de FT, depuis un fichier yaml
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script (todo: trouver une meilleure solution)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "..", CREDENTIALS_FILE)
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/

with open(file_path, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)


# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
launch_get_referentiel_appellations_rome = 0
launch_get_referentiel_pays = 0
launch_get_offres = 0
launch_merge_all_json_into_one = 1


if launch_get_referentiel_appellations_rome:
    get_referentiel_appellations_rome(token)

#################################################################################################################################

if launch_get_referentiel_pays:
    get_referentiel_pays(token)

#################################################################################################################################


if launch_get_offres:
    file_path = os.path.join(current_directory, "code_appellation_libelle.yml")

    with open(file_path, "r") as file:
        content = yaml.safe_load(file)
        code_appellation_libelle = content["code_appellation_libelle"]  # functions.py
        codes_list = [i["code"] for i in code_appellation_libelle]

    for code in codes_list:
        get_offres(
            token,
            code_appellation_libelle,
            filter_params={
                #### codes
                "appellation": code,  # Code appellation ROME de l’offre
                # "codeNAF": "",  # Code NAF de l’offre, (format 99.99X)
                # "codeROME": "",  # Code ROME de l’offre, voir le référentiel des métiers ci-dessous
                #### localisation
                # "paysContinent" : Pays ou continent de l’offre
                "paysContinent": "01",  # pour la France (non restreint à la métropôle)
                # "paysContinent": "02",  # pour l'Allemagne (presque pas d'offre)
                # "paysContinent": "04",  # pour la Belgique (presque pas d'offre)
                # "paysContinent": "07",  # pour l'Espagne (presque pas d'offre)
                # "paysContinent": "23",  # pour la Suisse (presque pas d'offre)
                # "paysContinent": "61",  # pour le US (presque pas d'offre)
                # "paysContinent": "83",  # pour le Japon (presque pas d'offre)
                # "commune": "",  # Code INSEE de la commune
                # "departement": "",  # Département de l’offre (Jusqu'à 5 valeurs possibles, séparées par une virgule)
                # "distance": "",  # Distance à la commune (pris en compte uniquement si une commune est renseignée, plus d'information dans la documentation)
                # "inclureLimitrophes": "",  # Inclure les départements limitrophes dans la recherche
                # "region": "",  # Région de l’offre
                #### contrat
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
                #### experience
                # "experience": "",  # Niveau d’expérience demandé, (1 moins d'un an, 2 de 1 à 3 ans, 3 plus de 3 ans)
                # "experienceExigence": "D",  # Exigence d'expérience (D débutant accepté, S expérience souhaitée, E expérience exigée)
                #### date de création # todo : jouer sur les dates pour voir si on peut récupérer les vieilles offres
                # "maxCreationDate": "",  # Date maximale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "minCreationDate": "",  # Date minimale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "publieeDepuis": "",  # Recherche les offres publiées depuis maximum « X » jours
                #### misc.
                # "sort": "",  # Tri selon 3 façons différentes
                # "accesTravailleurHandicape": True,  # Offres pour lesquelles l’employeur est handi friendly
                # "modeSelectionPartenaires": "",  # Énumération (INCLUS ou EXCLU) - Mode de sélection des partenaires.
                # "motsCles": "data",  # Recherche de mots clés dans l’offre, voir documentation
                # "niveauFormation": "",  # Niveau de formation demandé
                # "offresMRS": "",  # Uniquement les offres d'emplois avec méthode de recrutement par simulation proposée
                # "offresManqueCandidats": "",  # Filtre sur les offres difficiles à pouvoir
                # "origineOffre": "",  # Origine de l'offres
                # "partenaires": "",  # Chaine de caractères - Liste des codes partenaires dont les offres sont à inclure ou exclure en fonction du mode de sélection associé et du filtre de l’origine de l’offre # noqa
                # "permis": "",  # Permis demandé
                # "qualification": "",  # Qualification du poste (0 non-cadre, 9 cadre)
                # "secteurActivite": "",  # Division NAF de l’offre (2 premiers chiffres)
                # "theme": "",  # Thème ROME du métier
                # "domaine": "",  # Domaine de l’offre
                # "entreprisesAdaptees": "",  # Filtre sur les offres dont les entreprises sont adaptées
            },
        )

# notes :
# pour filtrer qu'en France métropolitaine :
#   - on ne peut pas filtrer sur les 13 régions en une fois (une seule région possible dans la requête)
#   - on ne peut mettre que 5 départements d'un coup

#################################################################################################################################


if launch_merge_all_json_into_one:

    merged_json_filename = "_offres_merged.json"
    json_files_directory = os.path.join(current_directory, "outputs", "offres")
    merged_json_filename_path = os.path.join(json_files_directory, merged_json_filename)

    merge_all_json_into_one(json_files_directory, merged_json_filename)
