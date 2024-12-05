import os

import yaml

from functions import filtrer_offres_selon_liste, get_appellations, get_bearer_token, get_offres

# Récupération des credentials données sur le site de FT, depuis un fichier yaml
CREDENTIALS_FILE = "api_credentials_minh.yml"  # à modifier selon qui lance le script (todo: trouver une meilleure solution)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "..", CREDENTIALS_FILE)

with open(file_path, "r") as file:
    creds = yaml.safe_load(file)

IDENTIFIANT_CLIENT = creds["API_FRANCE_TRAVAIL"]["IDENTIFIANT_CLIENT"]
CLE_SECRETE = creds["API_FRANCE_TRAVAIL"]["CLE_SECRETE"]

# Lancer les fonctions plus simplement ("= 1" pour lancer)
launch_get_bearer_token = 0
launch_get_appellations = 0
launch_get_offres = 0
launch_filtrer_offres_selon_liste = 1

################################################################################################################################################################

if launch_get_bearer_token:
    token = get_bearer_token(
        client_id=IDENTIFIANT_CLIENT,
        client_secret=CLE_SECRETE,
        scope="o2dsoffre api_offresdemploiv2",  # scopes définis dans https://francetravail.io/produits-partages/catalogue/offres-emploi/documentation#/
    )

################################################################################################################################################################

if launch_get_appellations:
    get_appellations(token)

################################################################################################################################################################


if launch_get_offres:
    # toutes les offres des métiers de la data
    codes = [
        #### métier Data Engineer
        "404278",  # { "code": "404278", "libelle": "Data engineer" }
        "404277",  # { "code": "404277", "libelle": "Big data engineer" }
        "404282",  # { "code": "404282", "libelle": "Ingénieur / Ingénieure big data" }
        "404284",  # { "code": "404284", "libelle": "Ingénieur / Ingénieure données"}
        #### autres métiers de la data
        "38095",  # { "code": "38095", "libelle": "Analyste décisionnel - Business Intelligence" }
        "38970",  # { "code": "38970", "libelle": "Data Miner" }
        "38971",  # { "code": "38971", "libelle": "Data analyst" }
        "38972",  # { "code": "38972", "libelle": "Data scientist" }
        "38975",  # { "code": "38975", "libelle": "Data manager" }
        "38977",  # { "code": "38977", "libelle": "Développeur / Développeuse Big Data" }
        "404271",  # { "code": "404271", "libelle": "Expert / Experte en sciences des données"}
        "404273",  # { "code": "404273", "libelle": "Explorateur / Exploratrice de données"}
        "404274",  # { "code": "404274", "libelle": "Ingénieur / Ingénieure data scientist" }
        "404275",  # { "code": "404275", "libelle": "Analyste qualité des données" }
        "404276",  # { "code": "404276", "libelle": "Architecte big data" }
        "404279",  # { "code": "404279", "libelle": "Docteur big data" }
        "404280",  # { "code": "404280", "libelle": "Expert / Experte big data" }
        "404281",  # { "code": "404281", "libelle": "Expert / Experte technique big data" }
        "404283",  # { "code": "404283", "libelle": "Ingénieur / Ingénieure dataviz" }
        "404285",  # { "code": "404285", "libelle": "Ingénieur / Ingénieure en développement big data" }
        "404286",  # { "code": "404286", "libelle": "Responsable architecture conception data" }
        "404287",  # { "code": "404287", "libelle": "Responsable big data" }
        "404288",  # { "code": "404288", "libelle": "Développeur / Développeuse data" }
        "404289",  # { "code": "404289", "libelle": "Analyste scientifique des données" }
        "404289",  # { "code": "404289", "libelle": "Analyste scientifique des données"}
        "404291",  # { "code": "404291", "libelle": "Data Protection Officer" }
        "404939",  # { "code": "404939", "libelle": "Biostatisticien / Biostatisticienne data manager" }
        "405222",  # { "code": "405222", "libelle": "Data analyst de la performance" }
        "489091",  # { "code": "489091", "libelle": "Database administrator" }
        #### rien à voir avec la data
        # "11573",  # {"code": "11573", "libelle": "Boulanger / Boulangère"}
        # "17406",  # {"code": "17406", "libelle": "Ouvrier boucher / Ouvrière bouchère"}
        # "10438",  # {"code": "10438", "libelle": "Agent / Agente de destruction d'insectes"},
    ]

    for code in codes:
        get_offres(
            token,
            filter_params={
                #### codes
                "appellation": code,  # Code appellation ROME de l’offre, voir le référentiel ci-dessous
                # "codeNAF": "",  # Code NAF de l’offre, (format 99.99X)
                # "codeROME": "",  # Code ROME de l’offre, voir le référentiel des métiers ci-dessous
                #### localisation
                # "commune": "",  # Code INSEE de la commune, voir le référentiel ci-dessous
                # "departement": "75",  # Département de l’offre, voir le référentiel ci-dessous
                # "distance": "",  # Distance à la commune (pris en compte uniquement si une commune est renseignée, plus d'information dans la documentation)
                # "inclureLimitrophes": "",  # Inclure les départements limitrophes dans la recherche
                # "paysContinent": "",  # Pays ou continent de l’offre, voir le référentiel ci-dessous
                # "region": "",  # Région de l’offre, voir le référentiel ci-dessous
                #### contrat
                # "dureeContratMax": "",  # Recherche les offres avec une durée de contrat maximale (format double de 0 à 99 bornes incluses)
                # "dureeContratMin": "",  # Recherche les offres avec une durée de contrat minimale (format double de 0 à 99 bornes incluses)
                # "dureeHebdo": "",  # Type de durée du contrat de l'offre
                # "dureeHebdoMax": "",  # Recherche les offres avec une durée maximale (format HHMM)
                # "dureeHebdoMin": "",  # Recherche les offres avec une durée minimale (format HHMM)
                # "tempsPlein": "",  # Temps plein ou partiel
                # "natureContrat": "",  # Code de la nature du contrat, voir le référentiel ci-dessous
                # "typeContrat": "",  # Code du type de contrat, voir le référentiel ci-dessous
                # "periodeSalaire": "",  # Période pour le calcul du salaire minimum (M Mensuel, A Annuel, H Horaire, C Cachet). Si cette donnée est renseignée, le salaire minimum est obligatoire. # noqa
                # "salaireMin": "",  # Salaire minimum recherché. Si cette donnée est renseignée, le code du type de salaire minimum est obligatoire.
                #### experience
                # "experience": "",  # Niveau d’expérience demandé, (1 moins d'un an, 2 de 1 à 3 ans, 3 plus de 3 ans)
                # "experienceExigence": "D",  # Exigence d'expérience (D débutant accepté, S expérience souhaitée, E expérience exigée)
                #### date de création
                # "maxCreationDate": "",  # Date maximale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "minCreationDate": "",  # Date minimale pour laquelle rechercher des offres (format yyyy-MM-dd'T'hh:mm:ss'Z')
                # "publieeDepuis": "",  # Recherche les offres publiées depuis maximum « X » jours
                #### misc.
                # "accesTravailleurHandicape": True,  # Offres pour lesquelles l’employeur est handi friendly
                # "modeSelectionPartenaires": "",  # Énumération (INCLUS ou EXCLU) - Mode de sélection des partenaires.
                # "motsCles": "data",  # Recherche de mots clés dans l’offre, voir documentation
                # "niveauFormation": "",  # Niveau de formation demandé, voir le référentiel ci-dessous
                # "offresMRS": "",  # Uniquement les offres d'emplois avec méthode de recrutement par simulation proposée
                # "offresManqueCandidats": "",  # Filtre sur les offres difficiles à pouvoir
                # "origineOffre": "",  # Origine de l'offres
                # "partenaires": "",  # Chaine de caractères - Liste des codes partenaires dont les offres sont à inclure ou exclure en fonction du mode de sélection associé et du filtre de l’origine de l’offre # noqa
                # "permis": "",  # Permis demandé, voir le référentiel ci-dessous
                # "qualification": "",  # Qualification du poste (0 non-cadre, 9 cadre)
                # "secteurActivite": "",  # Division NAF de l’offre (2 premiers chiffres), voir le référentiel ci-dessous
                # "sort": "",  # Tri selon 3 façons différentes
                # "theme": "",  # Thème ROME du métier, voir le référentiel ci-dessous
                # "domaine": "",  # Domaine de l’offre, voir le référentiel ci-dessous
                # "entreprisesAdaptees": "",  # Filtre sur les offres dont les entreprises sont adaptées
            },
        )

################################################################################################################################################################


if launch_filtrer_offres_selon_liste:
    data_engineer = {
        "a_inclure": [  # traiter ça par regex ? à discuter
            "Data Engineer",
            "Data Ingineer",  # typo recruteur
            "Data Ingénieur",
            "Data Ingénieur(e)",
            "Data Ingénieur-e",
            "Data Ingenieur",
            "Data Ingenieur(e)",
            "Data Ingenieur-e",
            "Ingénieur Data",
            "Ingénieur(e) Data",
            "Ingénieur-e Data",
            "Ingenieur Data",
            "Ingenieur(e) Data",
            "Ingenieur-e Data",
            "Ingénieur De Donnée",  # sans "s" (volontaire)
            "Ingénieur(e) De Donnée",
            "Ingénieur-e De Donnée",
            "Ingenieur De Donnée",
            "Ingenieur(e) De Donnée",
            "Ingenieur-e De Donnée",
            "Ingénieur Donnée",
            "Ingénieur(e) Donnée",
            "Ingénieur-e Donnée",
            "Ingenieur Donnée",
            "Ingenieur(e) Donnée",
            "Ingenieur-e Donnée",
            "Ingénieur / Ingénieure Donnée",
            "Ingénieur / Ingénieure Data",
            "Ingénieur - Ingénieure Donnée",
            "Ingénieur - Ingénieure Data",
            "Ingénieur/Ingénieure Donnée",
            "Ingénieur/Ingénieure Data",
            "Ingénieur-Ingénieure Donnée",
            "Ingénieur-Ingénieure Data",
            "Ingenieur / Ingenieure Donnée",
            "Ingenieur / Ingenieure Data",
            "Ingenieur - Ingenieure Donnée",
            "Ingenieur - Ingenieure Data",
            "Ingenieur/Ingenieure Donnée",
            "Ingenieur/Ingenieure Data",
            "Ingenieur-Ingenieure Donnée",
            "Ingenieur-Ingenieure Data",
            "Ingénieur Big Data",
            "Ingenieur Big Data",
            "Big Data",  # inclut "Développeur Big Data" (à exclure)
            "BigData",
            "Data Pipeline",
            # "Spark"
            #### à inclure ?
            # "Ingénieur En Traitement De Données",
            # "Expert En Bases De Données MongoDB",
            # "Expert Bases De Données PostGre",
            # "Data Expert",
            # "Administrateur De Base De Données",
            # "Administrateur de Base de Données",
            # "Administrateur des données centrales",
            # "Administrateur bases de données",
            # "Administrateur base de données",
            # "Gestionnaire de base de données",
            # "Gestionnaire Base de données",
            # "Administrateur(trice) Base de données MySQL / PostGRE / MongoDB",
        ],
        "a_exclure": [
            "Ingénieur Data Scientist",
            "Ingénieur Data Center",
            "Développeur",
            "Chef De Projet",
            "Architecte",
        ],
    }

    data_analyst = {
        "a_inclure": [
            "Analyste Décisionnel",
            "Data Analyst",
            "Data-Analyst",
            "Analyste Data",
            "Analystes Data",
            "Analyse De Donnée",  # sans "s" (volontaire)
            "Analyste De Donnée",
            "Data Viz",
            "DataViz",
            "Data Visualisation",
            "Data Vizualisation",
            "Business Intelligence",
            "Power Bi",
        ],
        "a_exclure": [
            "Développeur",
            "Business Analyst",
            "Analyste Fonctionnel",
            "Analyste Développeur",
            "Analyste Programmeur",
            "Analyste SOC",
            "Analyste trésorerie",
            "Analyste cybersécurité",
            "Informaticien",
        ],
    }

    data_scientist = {
        "a_inclure": [
            "Data Scientist",
            "Data-Scientist",
            "Datascientist",
            "Data-Science",
            "Data Science",
            "Scientifique de données",
            "Scientifique des données",
        ],
        "a_exclure": [
            # "analyst"
        ],
    }

    # strings_a_inclure_exclure_dans_intitule_offre = data_engineer  # 134 offres
    strings_a_inclure_exclure_dans_intitule_offre = data_analyst  # 143 offres
    # strings_a_inclure_exclure_dans_intitule_offre = data_scientist  # 60 offres

    directory = os.path.join(current_directory, "outputs", "offres")

    filtrer_offres_selon_liste(directory, strings_a_inclure_exclure_dans_intitule_offre)
