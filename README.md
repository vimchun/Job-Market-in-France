# Présentation du projet

J'ai réalisé ce projet seul de bout en bout, dans le cadre de ma formation "Data Engineer" chez Data Scientest.

Les objectifs sont globalement de :

  - mettre en place un pipeline ETL/ELT pour récupérer les offres d'emploi par API sur https://francetravail.io/data/api, étudier les attributs disponibles et faire le diagramme UML, effectuer des transformations en amont ou en aval de l'écriture des données dans une base de données Postgres,

  - consommer les données avec la mise en place de rapports avec Power BI,

  - travailler avec un environnement docker,

  - mettre en place une API pour qu'un utilisateur puisse requêter la base de données via une interface graphique (ici avec FastAPI),

  - orchestrer les tâches avec Airflow.


Pour alléger cette page principale, une autre page avec des informations supplémentaires est disponible dans cette ![page](readme_files/README_additional_notes.md)


Le plan suivant présente un plan logique plutôt que de présenter les étapes qui ont été effectuées par ordre chronologique :

todo : toc



# fourre tout à trier

explication choix postgres (ex : intégration avec airflow)


# Slideshow

todo : à faire fin juillet pour la soutenance


# Environnement technique

Développements et tests sous :
  - Windows 11 + WSL + Docker Desktop
  - Environnement virtuel, Python 3.12.9 (février 2025)
  - Airflow 3.0.2 (juin 2025), https://github.com/apache/airflow/releases


## Getting started

- Clone le projet.

- Mettre en place la configuration docker :


```bash
  # Pour initialiser Airflow et démarrer les services docker :
  #  (peut prendre du temps à avoir les services fonctionnels)
  ./scripts/docker_compose_down_up.sh


  # Pour redémarrer tous les services
  ./scripts/restart_all_docker_services.sh
  ```

- Créer la connexion `postgres` :

```bash
  ./scripts/create_postgres_connection_on_airflow.sh
  ```

- On pourra vérifier que la connexion est bien créée via la GUI comme montré sur le screenshot suivant :

  ![airflow_edit_connection](readme_files/screenshots/airflow_gui_edit_connection.png)

   (si la connexion n'est pas bien définie, alors le `DAG 2` posera problème)


Dans l'idéal, il aurait fallu créer cette connexion de manière "encore plus automatique" avec une tâche dans le `DAG 2` (cela permettra de ne pas avoir à exécuter le script précédent), mais certaines problématiques nous en empêchent. Ceci est documenté ![ici](readme_files/README_additional_notes.md#création-automatique-de-connexion-postgres)


## Arborescence du projet sans la partie liée à la conf Docker

todo : revoir à la fin du projet

  ```bash
  .
  ├── airflow/                         # application Airflow
  │   ├── config                       # contient le fichier fichier de conf "airflow.cfg"
  │   ├── dags                         # contient "DAG 1" et "DAG 2"
  │   ├── data
  │   │   ├── outputs                  # contient les jsons récupérés par API, et le json qui les aggrège avec les transformations Python
  │   │   └── resources                # contient les différents fichiers nécessaires au lancement du DAG 1
  │   ├── logs                         # contient les logs des DAGs
  │   └── plugins                      # contient les plugins (dossier non utilisé pour le moment)
  │  
  ├── fastapi/                         # application FastAPI
  │   ├── sql_requests                 # requêtes SQL utilisées par le script fastapi
  │   ├── locations_information        # point de montage (volume)  # todo : à renommer en "locations_information_mount" ?
  │   └── main.py                      # script fastapi
  ```


## Configuration Docker

Le fichier `docker-compose.yml` décrit les différents services déployés : `postgres`, `fastapi`, `redis`, `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `airflow-cli`, `flower`.

- Arborescence avec les éléments liés à la dockerisation :

```bash
  .
  ├── airflow/                         # application Airflow
  │   ├── requirements.txt             # dépendances nécessaires pour le Dockerfile
  │   └── Dockerfile                   # construction du conteneur Airflow
  │  
  ├── fastapi/                         # application FastAPI
  │   ├── requirements.txt             # dépendances nécessaires pour le Dockerfile
  │   └── Dockerfile                   # construction du conteneur FastAPI
  │  
  └── docker-compose.yml               # orchestration docker pour postgres + fastapi + les services Airflow
  ```

- Notes concernant la configuration `fastapi` :

  - Lors de la phase de développement :
    - `Dockerfile` :
      - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]` (avec l'option `--reload` pour ne pas avoir à relancer la commande après une modification)
    - `docker-compose.yml` :
      - avec les montages de volumes pour ne pas avoir à relancer le docker-compose après chaque modification de fichiers sql

  - Quand les développements seront terminés (phase de prod) :
    - `Dockerfile` :
      - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` (sans l'option `--reload`)
      - `COPY` du script python, et des fichiers nécessaires dans le conteneur (fichier csv, fichiers sql), au lieu de passer par des volumes



# Workflow du projet avec Airflow

## Avant Airflow

Avant d'appliquer Airflow au projet, 2 scripts python étaient nécessaires.
Pour résumer et simplifier ce qu'ils faisaient ("simplifier" ici car ces scripts ont été remplacés par des DAGs qu'on détaillera après) :
  - Le premier récupérait les données de France Travail, faisait des transformations, et chargeait les offres d'emploi dans un json.
  - Le second lisait le json puis écrivait les offres d'emploi dans la base de données, et effectuait un deuxième lot de transformations à partir de fichier sql.

  ![screenshot du workflow](readme_files/screenshots/workflow.png)


Reprendre ces scripts pour avoir Airflow dans le projet a été bénéfique :
  - amélioration des fonctions définis
  - code plus compréhensible : factorisation de code, changement des noms de variables, revue des commentaires
  - meilleure façon d'écrire les offres d'emploi dans le json
  - meilleure gestion des cas d'erreur, et gestion d'erreur auquel on n'était pas confronté auparavant (exemple avec la parallélisation des requêtes et les erreurs 429 `Too much requests`)
  - simplification des requêtes sql


## Avec Airflow

Les bénéfices d'Airflow sur ce projet sont multiples et évidents :

  - avoir une vision claire du workflow complet à travers la vue Graph du DAG
  - voir quelle fonction pose problème d'un coup d'oeil en cas d'échec et voir les logs associés à la tâche en échec
  - lancer le workflow complet à la fréquence désirée (par exemple, tous les jours à 20h)
  - et surtout obtenir un gain de temps avec la parallélisation de certaines tâches :
    - requêtes API pour récupérér les offres d'emploi pour x métiers en parallèle,
    - requêtes SQL pour remplir x tables en parallèle,
    - requêtes SQL pour effectuer x transformations en parallèle.


## Version utilisée

Au moment d'écrire les DAGs, il y avait deux versions majeures : la 2.11.0 et la 3.0.1.
Finalement, le choix se portera sur la version 3.0.x car cette nouvelle branche a des évolutions majeures (https://airflow.apache.org/blog/airflow-three-point-oh-is-here/).


## Description du worflow des DAGs

Ci-dessous le nom d'une `tâche` avec une description.

Pour alléger le texte, on écrira :

- `fichier_existant.json` : fichier json aggrégeant les fichiers jsons téléchargés
- `dossier_A` : dossier contenant tous les fichiers json téléchargés par api
- `dossier_B` : dossier contenant le json fichier_existant.json


### DAG 1

#### Task group "setup"

##### Task group "check_files_in_folders"


- `S1_delete_all_in_one_json`

  - Suppression du fichier `all_in_one.json` s'il existe


- `S1_check_csv_file_exists`, `S1_check_appellation_yaml_file_exists`, `S1_check_credentials_yaml_file_exists`

  - Vérification de la présence de ces fichiers :
    - si un des fichiers n'existe pas : fin du DAG (exception levée)


- `S1_count_number_of_json_file`

  - Vérification du nombre de fichiers json dans le `dossier_B` :
    - s'il y a plusieurs fichiers json : fin du DAG (exception levée).
    - s'il y a 0 ou 1 fichier json `fichier_existant.json` : on continue et on retourne "count" (nombre de fichiers json).



##### Task group "after_checks"

- `S2_remove_all_json_files`

  - Suppression des fichiers json dans le `dossier_A`.
    - Après suppression, on vérifie qu'il n'y a plus de fichier json, sinon fin du script.


- `S2_load_appellations_yaml_file`

  - Chargement fichier yaml avec 61 métiers.


- `S2_get_creds_from_yaml_file`

  - Récupération des credentials depuis le fichier.


- `S2_get_token`

  - Récupération du token API.



#### Task group "ETL"

- `A1_get_offers`

  - Récupération et écriture des offres d'emploi dans des fichiers json dans le dossier_A + vérification validité fichiers json [requests].


- `A2_all_json_in_one`

  - Consolidation de tous les fichiers json du dossier_A en un seul fichier json data.json dans le dossier_B et suppression des doublons [pandas].


- `A3_only_metropole`

  - Conservation uniquement dans les offres d'emploi en France Métropolitaine data.json [pandas].


- `A4_add_location_attrs`

  - Ajout d'attributs dans data.json : `nom_commune`, `nom_ville`, `code_departement`, `nom_departement`, `code_region`, `nom_region` [pandas/geopy]
    (à partir du code insee, coordonnées GPS et autres infos).


- `A5_add_dateExtraction_attr`

  - Ajout d'un attribut dans data.json : `date_extraction` [pandas]
    (pour connaitre la date d'extraction et la date où on écrit la première fois dans la base).


- `A6_0_or_1_json_on_setup`

  - Vérification du nombre de fichiers json dans le `dossier_B`.


##### Task group "0_file_in_folder"

- Cas où il n'y a pas de fichier json dans le `dossier_B`.

  - `A8_add_date_premiere_ecriture_attr`

    - Ajout d'un attribut dans data.json : `date_premiere_ecriture` [pandas].


  - `A9_rename_json_file`

    - Renommage du fichier.


##### Task group "1_file_in_folder"

- Cas où il y a 1 fichier json `fichier_existant.json`.

  - `A7_special_jsons_concat`

    - Concaténation spéciale entre le json existant et le nouveau json [pandas] + renommage fichier final + déplacement ancien json existant dans dossier "archives".


  - `A8_add_date_premiere_ecriture_attr`

    - Ajout d'un attribut dans data.json : date_premiere_ecriture [pandas].

      - Notes : l'attribut `date_premiere_ecriture` prendra la date du jour pour toutes les nouvelles offres, et conservera l'ancienne valeur pour les anciennes offres.


- `A10_write_to_history`

  - Ecriture de l'historique du fichier json dans `_json_files_history.csv` (ajout nom json restant dans le dossier et le nombre de lignes).



### DAG 2


#### setup

- `check_only_one_json_in_folder`

  - Vérification qu'il n'y ait qu'un json `fichier_existant.json` dans `dossier_B`


- `remove_all_split_jsons`

  - Suppression des fichiers json dans le `dossier_A`.


- `split_large_json`

  - split le gros fichier json final en plusieurs jsons dédiés pour les tâches suivantes du DAG.
  - L'intérêt est que toutes les tâches ne lisent pas le même gros fichier json, et que chaque tâche lise chacun son fichier json dédié.

- `SQLExecuteQueryOperator()` avec le fichier `sql/create_all_tables.sql`

  - Création de toutes les tables du projet si elles n'existent pas.



#### without_junction

Ce groupe exécute en parallèle les tâches suivantes, qui consistent à récupérer les informations dans les fichiers json dédiés (générés par la tâche `split_large_json`) et exécutent des `INSERT INTO` dans les tâches dédiés :

- `OffreEmploi`
- `Contrat`
- `Entreprise`
- `Localisation`
- `DescriptionOffre`



#### with_junction

Ce groupe exécute les actions suivantes :

Prenons pour exemple, `Competence` puis `Offre_Competence`

  1/ `INSERT INTO` pour la table de dimension
  2/ requête pour connaitre la correspondance entre `offre_id` et `competence_id` avant de faire des `INSERT INTO` pour la table de liaison
  3/ conservation de l'offre la plus récente, si `competence_id` a évolué


- `Competence` puis `Offre_Competence`
- `Experience` puis `Offre_Experience`
- `Formation` puis `Offre_Formation`
- `QualiteProfessionnelle` puis `Offre_QualiteProfessionnelle`
- `Qualification` puis `Offre_Qualification`
- `Langue` puis `Offre_Langue`
- `PermisConduire` puis `Offre_PermisConduire`


#### transformations

Plusieurs `SQLExecuteQueryOperator()` qui exécutent séquentiellement les tâches suivantes, dont les fichiers SQL du dossier `airflow/dags/sql` sont :

  - `update_descriptionoffre_metier_data_DE`
  - `update_descriptionoffre_metier_data_DA`
  - `update_descriptionoffre_metier_data_DS`
  - `update_contrat_salaires_min_max`
  - `update_descriptionoffre_column_liste_mots_cles`




# Extraction des données par API

- France Travail (https://francetravail.io/data/api) met à disposition plusieurs APIs, dont "Offres d'emploi v2" (`GET https://api.francetravail.io/partenaire/offresdemploi`).

- Le endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search` permet de récupérer les offres d'emploi actuelles selon plusieurs paramètres dont :

  - le code des appellations ROME pour filtrer par métier (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations`) :

    ```json
    { "code": "38971",  "libelle": "Data_Analyst" },
    { "code": "38972",  "libelle": "Data_Scientist" },
    { "code": "404278", "libelle": "Data_Engineer" },
    { "code": "38975",  "libelle": "Data_Manager" },
    ...
    ```

  - le code des pays (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/pays`) :

    ```json
    { "code": "01", "libelle": "France" },     // inclut les offres en France d'outre-mer et en Corse
    { "code": "02", "libelle": "Allemagne" },  // les pays étrangers ne retournent malheureusement pas d'offre sur les métiers à analyser
    ...
    ```

  - le paramètre `range` qui limite les résultats à 150 offres par requête (avec un status code à `206` si une requête renvoie plus de 150 offres), sachant que l'API ne permet de récupérer que 3150 offres au maximum par appellation ROME.

    - Ainsi, si une requête renvoit 351 offres, il faut enchainer 3 requêtes pour obtenir toutes les offres (la première requête donne les offres `0-149` (status code 206), la deuxième donne les offres `150-299` (status code 206), et la troisième donne les offres `300-350` (status code 200)).


- Cet API retourne des offres d'emploi sous forme de documents json avec énormément d'attributs dont l'identifiant de l'offre, son intitulé, sa description, le lieu de travail, des informations sur l'entreprise et sur le contrat, les compétences demandées et l'expérience nécessaires, etc...

- Toutefois, l'API retourne aussi énormément d'offres sans lien avec le métier renseigné en paramètre (par exemple, une requête renseignant l'appellation `Data Engineer` peut renvoyer une offre telle que `Product Owner` car les termes `Data Engineer` peuvent être présents dans la description de l'offre d'emploi).

- On va requêter ainsi un large panel de métiers, dont 29 ayant un lien avec la data, et 32 ayant un lien avec les métiers de la tech (dev, sécurité, devops...), pour maximiser les chances d'obtenir le plus d'offres d'emploi ayant un lien avec les métiers `DE`, `DA` et `DS`, et aussi pour avoir une base de données plus conséquente.

  - En effet, des offres de `Data Engineer` peuvent être présentes en requêtant l'appellation `Data Manager` par exemple.

- On obtient finalement 61 fichiers json contenant toutes les offres d'emploi liées ou pas à la data, pour la France et DOM-TOM uniquement, l'API de France Travail ne renvoyant quasiment pas d'offre d'emploi pour les autres pays.

- Plusieurs transformations seront effectuées par la suite : ![voir ici](#transformations-des-données-en-amont-côté-python)


- Notes :

  - Les paramètres liés aux dates (`minCreationDate`, `maxCreationDate`, `publieeDepuis`) ne permettent pas d'obtenir des offres expirées (par exemple celles qui ont permis de recruter quelqu'un).

  - Les offres d'emploi retournées peuvent provenir soit de `FRANCE TRAVAIL`, soit des `partenaires` (par exemple `CADREMPLOI`, `DIRECTEMPLOI`, `INDEED`, etc...)


# Transformations des données

## Transformations des données en amont (côté Python)

Ces transformations sont faites dans le `DAG 1`, faites via Python et en amont du chargement dans la base Postgres :

  - Concaténation des 61 fichiers json dans un seul fichier json, avec suppression des doublons

  - Conservation des offres en France Métropolitaine uniquement, ![détails ici](readme_files/README_additional_notes.md#conservation-des-offres-en-France-Métropolitaine-uniquement)

  - Ajout des attributs de localisation des offres (noms et codes des villes, départements, départements et régions), ![détails ici](readme_files/README_additional_notes.md#attributs-de-localisation-des-offres-noms-et-codes-des-villes-communes-départements-et-régions)

  - Ajout des attributs `date_premiere_ecriture` et `date_extraction` :

    - `date_extraction` aura la date du jour à laquelle le `DAG 1` a été lancé,
    - `date_premiere_ecriture` aura la date du jour pour toutes les nouvelles offres, mais prendra les anciennes valeurs pour les anciennes offres.



## Transformations des données en aval (côté SQL)

Ces transformations sont faites dans le `DAG 2`, faites via des requêtes SQL et effectuées en aval de l'écriture dans la base Postgres :

  - pour créer et écrire l'attribut `metier_data` : pour chaque offre, on comparera l'attribut `intitule_offre` avec des regex afin de déterminer s'il s'agit d'une offre pour un `Data Engineer`, un `Data Analyst`, ou un `Data Scientist`.

    - ![détails ici](readme_files/README_additional_notes.md#attribut-metier-data)

  - pour créer et écrire les attributs `salaire_min` et `salaire_max` en fonction d'un algorithme expliqué

    - ![détails ici](readme_files/README_additional_notes.md#attributs-salaire-min-et-salaire-max)



# Chargement des données dans une base de données relationnelle

- L'API de France Travail contient beaucoup d'attibuts pour une offre d'emploi, qui seront quasiment tous exploités par la suite.

  - Seuls les attributs liés aux `contacts` et aux `agences` ne seront pas conservés, n'apportant pas d'utilité.


- Pour la suite, une modélisation `snowflake` est utilisée, dont le diagramme UML est le suivant :

  ![screenshot diagramme UML](screenshots/UML.png)

- Le SGBD `PostgreSQL` sera utilisé. En effet :

  - PostgreSQL a été choisi pour ses performances, sa fiabilité et sa flexibilité.
  - En tant que solution open source, il offre une grande transparence et une forte extensibilité.
  - Il prend en charge des types de données complexes, respecte les principes ACID et bénéficie d’une communauté active assurant une évolution continue.

La base de données `francetravail` sera hébergée dans le conteneur Docker exécutant le service PostgreSQL.

- Les données issues du json généré avec le `DAG 1` seront récupérées et écrites en base avec la librairie `psycopg2`.


## Mise à jour de la base de données après récupération de nouvelles offres

Lors de la mise à jour de la base de données après récupération de nouvelles offres, on peut avoir des attributs dont les valeurs ont changé.

Par exemple, on peut avoir une offre avec un `experience_libelle` passer de `expérience exigée de 3 an(s)` à `débutant accepté`.

Même chose pour d'autres attributs.

Pour gérer cela, l'attribut `date_extraction` est écrit dans toutes les tables de liaison.
Ainsi, pour une offre, si un attribut d'une table de dimension associé à la table de liaison a évolué, alors on ne conservera que l'offre avec `date_extraction` le plus récent.

Plus de détails ![ici](readme_files/README_additional_notes.md#mise_à_jour_de_la_base_de_données_après_récupération_de_nouvelles_offres)


# Consommation des données

## Power BI

Power BI servira ici pour la data visualisation.

Ci-dessous des liens expliquant les différentes manipulations faites pour :

  - ![connecter Power BI avec la db postgres](readme_files/README_additional_notes.md#connexion-avec-la-db)

  - ![modifier le Model view](readme_files/README_additional_notes.md#model-view)

  - ![modifier le Table view](readme_files/README_additional_notes.md#table-view)

  - ![faire les transformations](readme_files/README_additional_notes.md#transformations)



## Analyse du jeu de données à travers des requêtes SQL

- voir le dossier `sql_requests/1_requests/offers_DE_DA_DS/`

- Au moins une requête sera faite pour chaque table de dimension pour mieux comprendre notre jeu de données.


# Création d'une API pour la db

- L'utilité peut par exemple être de requêter la db `francetravail` à travers l'interface OpenAPI (ex-swagger) pour récupérer certaines informations.

- Utilisation de `FastAPI`.

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.
