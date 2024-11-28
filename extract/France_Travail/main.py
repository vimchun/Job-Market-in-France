import os

import yaml

from functions import get_appellations, get_bearer_token, get_offres


# Récupération des credentials données sur le site de FT, depuis un fichier yaml
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script (todo: trouver une meilleure solution)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "..", CREDENTIALS_FILE)

with open(file_path, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]


###

token = get_bearer_token(
    client_id=IDENTIFIANT_CLIENT,
    client_secret=CLE_SECRETE,
    scope="o2dsoffre api_offresdemploiv2",  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
)


get_appellations(token)


# toutes les offres des métiers de la data
codes = [
    "38970",  # { "code": "38970", "libelle": "Data Miner" },
    "38971",  # { "code": "38971", "libelle": "Data analyst" },
    "38972",  # { "code": "38972", "libelle": "Data scientist" },
    "38975",  # { "code": "38975", "libelle": "Data manager" },
    "38977",  # { "code": "38977", "libelle": "Développeur / Développeuse Big Data" },
    "404274",  # { "code": "404274", "libelle": "Ingénieur / Ingénieure data scientist" },
    "404276",  # { "code": "404276", "libelle": "Architecte big data" },
    "404277",  # { "code": "404277", "libelle": "Big data engineer" },
    "404278",  # { "code": "404278", "libelle": "Data engineer" },
    "404279",  # { "code": "404279", "libelle": "Docteur big data" },
    "404280",  # { "code": "404280", "libelle": "Expert / Experte big data" },
    "404281",  # { "code": "404281", "libelle": "Expert / Experte technique big data" },
    "404282",  # { "code": "404282", "libelle": "Ingénieur / Ingénieure big data" },
    "404283",  # { "code": "404283", "libelle": "Ingénieur / Ingénieure dataviz" },
    "404285",  # { "code": "404285", "libelle": "Ingénieur / Ingénieure en développement big data" },
    "404286",  # { "code": "404286", "libelle": "Responsable architecture conception data" },
    "404287",  # { "code": "404287", "libelle": "Responsable big data" },
    "404288",  # { "code": "404288", "libelle": "Développeur / Développeuse data" },
    "404291",  # { "code": "404291", "libelle": "Data Protection Officer" },
    "404939",  # { "code": "404939", "libelle": "Biostatisticien / Biostatisticienne data manager" },
    "405222",  # { "code": "405222", "libelle": "Data analyst de la performance" },
    "489091",  # { "code": "489091", "libelle": "Database administrator" },
]

for code in codes:
    get_offres(
        token,
        filter_params={
            "accesTravailleurHandicape": False,  # Offres pour lesquelles l’employeur est handi friendly
            "appellation": code,  # Code appellation ROME de l’offre, voir le référentiel ci-dessous
            # "codeNAF": "",  # Code NAF de l’offre, (format 99.99X)
            # "codeROME": "",  # Code ROME de l’offre, voir le référentiel des métiers ci-dessous
            # "commune": "",  # Code INSEE de la commune, voir le référentiel ci-dessous
            # "departement": "",  # Département de l’offre, voir le référentiel ci-dessous
            # "distance": "",  # Distance à la commune (pris en compte uniquement si une commune est renseignée, plus d'information dans la documentation)
            # "domaine": "",  # Domaine de l’offre, voir le référentiel ci-dessous
            # "dureeContratMax": "",  # Recherche les offres avec une durée de contrat maximale (format double de 0 à 99 bornes incluses)
            # "dureeContratMin": "",  # Recherche les offres avec une durée de contrat minimale (format double de 0 à 99 bornes incluses)
            # "dureeHebdo": "",  # Type de durée du contrat de l'offre
            # "dureeHebdoMax": "",  # Recherche les offres avec une durée maximale (format HHMM)
            # "dureeHebdoMin": "",  # Recherche les offres avec une durée minimale (format HHMM)
            # "entreprisesAdaptees": "",  # Filtre sur les offres dont les entreprises sont adaptées
            # "experience": "",  # Niveau d’expérience demandé, (1 moins d'un an, 2 de 1 à 3 ans, 3 plus de 3 ans)
            # "experienceExigence": "",  # Exigence d'expérience (D débutant accepté, S expérience souhaitée, E expérience exigée)
            # "inclureLimitrophes": "",  # Inclure les départements limitrophes dans la recherche
            # "maxCreationDate": "",  # Date maximale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
            # "minCreationDate": "",  # Date minimale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
            # "modeSelectionPartenaires": "",  # Énumération (INCLUS ou EXCLU) - Mode de sélection des partenaires.
            # "motsCles": "data",  # Recherche de mots clés dans l’offre, voir documentation
            # "natureContrat": "",  # Code de la nature du contrat, voir le référentiel ci-dessous
            # "niveauFormation": "",  # Niveau de formation demandé, voir le référentiel ci-dessous
            # "offresMRS": "",  # Uniquement les offres d'emplois avec méthode de recrutement par simulation proposée
            # "offresManqueCandidats": "",  # Filtre sur les offres difficiles à pouvoir
            # "origineOffre": "",  # Origine de l'offres
            # "partenaires": "",  # Chaine de caractères - Liste des codes partenaires dont les offres sont à inclure ou exclure en fonction du mode de sélection associé et du filtre de l’origine de l’offre # noqa
            # "paysContinent": "",  # Pays ou continent de l’offre, voir le référentiel ci-dessous
            # "periodeSalaire": "",  # Période pour le calcul du salaire minimum (M Mensuel, A Annuel, H Horaire, C Cachet). Si cette donnée est renseignée, le salaire minimum est obligatoire. # noqa
            # "permis": "",  # Permis demandé, voir le référentiel ci-dessous
            # "publieeDepuis": "",  # Recherche les offres publiées depuis maximum « X » jours
            # "qualification": "",  # Qualification du poste (0 non-cadre, 9 cadre)
            # "region": "",  # Région de l’offre, voir le référentiel ci-dessous
            # "salaireMin": "",  # Salaire minimum recherché. Si cette donnée est renseignée, le code du type de salaire minimum est obligatoire.
            # "secteurActivite": "",  # Division NAF de l’offre (2 premiers chiffres), voir le référentiel ci-dessous
            # "sort": "",  # Tri selon 3 façons différentes
            # "tempsPlein": "",  # Temps plein ou partiel
            # "theme": "",  # Thème ROME du métier, voir le référentiel ci-dessous
            # "typeContrat": "",  # Code du type de contrat, voir le référentiel ci-dessous
        },
    )
