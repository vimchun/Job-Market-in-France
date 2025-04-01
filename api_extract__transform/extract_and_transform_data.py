import os

# from datetime import datetime
import yaml


# from colorama import init
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

# Récupération des credentials données sur le site de FT, depuis un fichier yaml
SCOPES_OFFRES = "o2dsoffre api_offresdemploiv2"  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script
current_directory = os.path.dirname(os.path.abspath(__file__))
credential_filename = os.path.join(current_directory, CREDENTIALS_FILE)
json_files_original_from_api_directory = os.path.join(current_directory, "outputs", "offres", "0--original_json_files_from_api")
generated_json_files_directory = os.path.join(current_directory, "outputs", "offres", "1--generated_json_files")

with open(credential_filename, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

token = get_bearer_token(client_id=IDENTIFIANT_CLIENT, client_secret=CLE_SECRETE, scope=SCOPES_OFFRES)


# Lancer les fonctions plus simplement ("= 1" pour lancer la fonction)
#  Notes :
#    - Il faut tout mettre à 1 pour le script de bout en bout.
#    - S'il n'y a pas de commentaire, la fonction met quelques secondes d'exécution.
launch_get_referentiel_appellations_rome = 0
launch_get_referentiel_pays = 0
launch_remove_all_json_files = 0
launch_create_csv__code_name__city_department_region = 0
#
launch_get_offres = 0  # ~ 20 minutes
launch_concatenate_all_json_into_one = 0
launch_add_date_extract_attribute = 1
launch_keep_only_offres_from_metropole = 1
launch_add_location_attributes = 1  # ~ 5 minutes

if launch_get_referentiel_appellations_rome:
    get_referentiel_appellations_rome(token)

#################################################################################################################################

if launch_get_referentiel_pays:
    get_referentiel_pays(token)

#################################################################################################################################

if launch_remove_all_json_files:
    remove_all_json_files(json_files_original_from_api_directory)

#################################################################################################################################

if launch_create_csv__code_name__city_department_region:
    create_csv__code_name__city_department_region()

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
"""
Noms de fichiers à écrire dans le dossier "api_extract__transform/outputs/offres" :

  - concatenate_all_json_into_one() :
        => json_generated_filename_0 = "2025-03-05--22h09__0__all__13639_offres.json"

  - add_date_extract_attribute() :
        => json_generated_filename_1 = "2025-03-05--22h09__1__all__13639_offres__with_date_extraction_attribute.json"

  - keep_only_offres_from_metropole() :
        => json_generated_filename_2 = "2025-03-05--22h09__2__only_metropole__13419_offres.json"

  - add_location_attributes() :
        => json_generated_filename_3 = "2025-03-05--22h09__3__with_location_attributes.json"
"""

if launch_concatenate_all_json_into_one:
    generated_json_filename_0 = concatenate_all_json_into_one(json_files_original_from_api_directory, generated_json_files_directory)
    print(f"  ====> Fichier généré : {generated_json_filename_0}")

#################################################################################################################################

if launch_add_date_extract_attribute:
    # Décommenter la ligne suivante si besoin de hardcoder (si "concatenate_all_json_into_one()" n'est pas exécutée)
    generated_json_filename_0 = "2025-03-12--21h13__0__all__13639_offres.json"

    """
    Noms de fichiers à écrire dans le dossier "api_extract__transform/outputs/offres" :

      - concatenate_all_json_into_one() :
            => json_generated_filename_0 = "2025-03-05--22h09__0__all__13639_offres.json"

      - add_date_extract_attribute() :
            => json_generated_filename_1 = "2025-03-05--22h09__1__all__13639_offres__with_date_extraction_attribute.json"
    """

    generated_json_filename_1_suffix = "__with_extraction_date_attribute.json"

    generated_json_filename_1 = add_date_extract_attribute(
        json_files_directory=generated_json_files_directory,
        json_filename=generated_json_filename_0,
        new_json_filename=f'{generated_json_filename_0.split(".json")[0]}{generated_json_filename_1_suffix}'.replace("__0__", "__1__"),
        date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
    )

    print(f"  -> fichier généré : {generated_json_filename_1}\n")

#################################################################################################################################

if launch_keep_only_offres_from_metropole:
    # Décommenter la ligne suivante si besoin de hardcoder (si "add_date_extract_attribute()" n'est pas exécutée)
    # generated_json_filename_1 = "2025-03-12--21h13__1__all__13639_offres__with_extraction_date_attribute.json"

    """
    Noms de fichiers à écrire dans le dossier "api_extract__transform/outputs/offres" :

      - add_date_extract_attribute() :
            => json_generated_filename_1 = "2025-03-05--22h09__1__all__13639_offres__with_date_extraction_attribute.json"

      - keep_only_offres_from_metropole() :
            => json_generated_filename_2 = "2025-03-05--22h09__2__only_metropole__13419_offres.json"
    """

    generated_json_filename_2_suffix = "__2__only_metropole__xxxxx_offres.json"

    generated_json_filename_2, df_lines_num = keep_only_offres_from_metropole(
        json_files_directory=generated_json_files_directory,
        json_filename=generated_json_filename_1,
        new_json_filename=f"{generated_json_filename_1.split('__1__')[0]}{generated_json_filename_2_suffix}",
    )

    # Le fichier s'appelle "2025-03-12--21h13__2__only_metropole__xxxxx_offres.json" (première élément retourné par "keep_only_offres_from_metropole()")
    # On remplace le nom du fichier en remplaçant le "xxxxx" avec le nombre de lignes du DataFrame (deuxième élément retourné par "keep_only_offres_from_metropole()")

    os.rename(
        os.path.join(generated_json_files_directory, generated_json_filename_2),
        os.path.join(generated_json_files_directory, generated_json_filename_2.replace("xxxxx", str(df_lines_num))),
    )

    generated_json_filename_2 = generated_json_filename_2.replace("xxxxx", str(df_lines_num))

    print(f"  -> fichier généré : {generated_json_filename_2}\n")


#################################################################################################################################

if launch_add_location_attributes:
    # Décommenter la ligne suivante si besoin de hardcoder (si "keep_only_offres_from_metropole()" n'est pas exécutée)
    # generated_json_filename_2 = "2025-03-12--21h13__2__only_metropole__13419_offres.json"

    """
    Noms de fichiers à écrire dans le dossier "api_extract__transform/outputs/offres" :

      - keep_only_offres_from_metropole() :
            => json_generated_filename_2 = "2025-03-05--22h09__2__only_metropole__13419_offres.json"

      - add_location_attributes() :
            => json_generated_filename_3 = "2025-03-05--22h09__3__with_location_attributes.json"
    """

    generated_json_filename_3_suffix = "__3__with_location_attributes.json"

    generated_json_filename_3 = add_location_attributes(
        json_files_directory=generated_json_files_directory,
        json_filename=generated_json_filename_2,
        new_json_filename=f"{generated_json_filename_2.split("__2__")[0]}{generated_json_filename_3_suffix}",
    )

    print(f"  -> fichier généré : {generated_json_filename_3}\n")
