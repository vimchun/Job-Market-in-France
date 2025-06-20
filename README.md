# Présentation du projet

J'ai réalisé ce projet seul de bout en bout, dans le cadre de ma formation "Data Engineer" chez Data Scientest.

Les objectifs sont globalement de :

  - mettre en place un pipeline ETL/ELT pour récupérer les offres d'emploi par API sur https://francetravail.io/data/api, étudier les attributs disponibles et faire le diagramme UML, effectuer des transformations en amont ou en aval de l'écriture des données dans une base de données Postgres,

  - consommer les données avec la mise en place de rapports avec Power BI,

  - travailler avec un environnement docker,

  - mettre en place une API pour qu'un utilisateur puisse requêter la base de données via une interface graphique (ici avec FastAPI),

  - orchestrer les tâches avec Airflow.



Le plan suivant présente un plan logique plutôt que de présenter les étapes qui ont été effectuées par ordre chronologique :

todo : toc

<!--

- Les étapes ont été les suivantes :

  - [1. Extraction des données par API et Transformations](readme_files/step_1__extract_and_transform_data.md)

  - [2. Chargement des données dans une base de données relationnelle](readme_files/step_2__load_data_to_database.md)

  - [3. Consommation des données](readme_files/step_3__data_consumption.md)

  - [4. Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL](readme_files/step_4__api.md)

  - [5. Orchestration avec Airflow](readme_files/step_5__airflow_orchestration.md)

  - [Arborescence](#arborescence-du-projet)
 -->


# fourre tout à trier

explication choix postgres (ex : intégration avec airflow)


# Slideshow

todo : à faire fin juillet pour la soutenance


# Environnement technique

Développements et tests sous :
  - Windows 11 + WSL + Docker Desktop
  - Environnement virtuel, Python 3.12.9 (04/02/2025)
  - Airflow 3.0.1 (12/05/2025), https://github.com/apache/airflow/releases


## Getting started

Clone

Lancer script : `./scripts/docker_compose_down_up.sh`

Définir la connexion dans la gui (todo : peut être fait par script ?)
https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#connections
https://airflow.apache.org/docs/apache-airflow/2.0.1/howto/connection.html#creating-a-connection-from-the-cli


(fait en 3.0.1)

Pour le `dag_id="dag_2_write_to_db"`, il faut définir dans la GUI une connexion Postgres, comme suit :

`Admin` > `Connections` > `Add Connection` :

  - Connection ID     : ma_connexion
  - Connection Type   : postgres
  - Standard Fieds
    - Host            : postgres  (note : c'est le nom du conteneur du service postgres, voir le fichier `docker-compose.yml`)
    - Login           : mhh
    - Password        : mhh
    - Port            : 5432
    - Database        : francetravail


  ![airflow_edit_connection](readme_files/screenshots/airflow_gui_edit_connection.png)


## Arborescence du projet

todo : faire à la fin du projet


# Workflow du projet avec Airflow

## Avant Airflow

Avant d'appliquer Airflow au projet, j'avais 2 scripts python.
Pour résumer et simplifier ce qu'il faisait ("simplifier" ici car ces scripts ont été remplacés par des DAGs qu'on détaillera après) :
  - le premier récupérait les données de France Travail, faisait des transformations, et chargeait les offres d'emploi dans un json
  - le second crée lit le json puis écrit les offres d'emploi dans la base de données, et effectue un deuxième lot de transformations à partir de fichier sql.

  ![screenshot du workflow](readme_files/screenshots/workflow.png)


Reprendre ces scripts pour avoir Airflow dans le projet a été bénéfique :
  - amélioration des fonctions définis
  - code plus compréhensible : factorisation de code, changement des noms de variables, revue des commentaires
  - meilleure façon d'écrire les offres d'emploi dans le json
  - meilleure gestion des cas d'erreur, et gestion d'erreur auquel on n'était pas confronté auparavant (exemple avec la parallélisation des requêtes et les erreurs 429 `too much requests`)
  - simplification des requêtes sql


## Avec Airflow

Les bénéfices d'Airflow sur ce projet sont multiples et évidents :

  - avoir une vision claire du workflow complet à travers la vue Graph du DAG
  - voir quelle fonction pose problème d'un coup d'oeil en cas d'échec et voir les logs associés à la tâche en échec
  - lancer le workflow complet à la fréquence désirée (par exemple, tous les jours à 20h)
  - et surtout paralléliser certaines tâches, donc gain de temps

Ici, ce dernier point permet un gain de temps considérable :
  - requêtes API pour récupérér les offres d'emploi pour x métiers en parallèle,
  - requêtes SQL pour remplir x tables en parallèle,
  - requêtes SQL pour effectuer x transformation.


## Version utilisée

Au moment d'écrire les DAGs, il y avait deux versions majeures : la 2.11.0 et la 3.0.1.
Finalement, le choix se portera sur la version 3.0.x car cette nouvelle branche a des évolutions majeures (https://airflow.apache.org/blog/airflow-three-point-oh-is-here/).


## Description des DAGs

### DAG 1

### DAG 2




## Notes techniques


### SQLExecuteQueryOperator vs PostgresOperator

Notes concernant l'erreur :

  ```bash
      from airflow.operators.postgres_operator import PostgresOperator
  ModuleNotFoundError: No module named 'airflow.operators.postgres_operator'
  ```

  causé par :

    ```python
    from airflow.operators.postgres_operator import PostgresOperator
    ```

Après s'être connecté sur le conteneur "worker" :

  ```bash
  default@0ab352f980fd:/opt/airflow$ pip list | grep apache-airflow-providers-postgres
  apache-airflow-providers-postgres         6.1.3
  ```

=> https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/


Change log : https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.2.0/changelog.html#

  ```md
  à partir de la 6.0.0 :
  Remove airflow.providers.postgres.operators.postgres.PostgresOperator. Please use airflow.providers.common.sql.operators.sql.SQLExecuteQueryOperator instead.
  ```


Conclusion : `PostgresOperator` est deprecated au profil de `SQLExecuteQueryOperator` avec la version `apache-airflow-providers-postgres` utilisée (6.1.3).
C'est ce qu'il faudra pour l'exécution des requêtes SQL.

  ```bash
  default@0ab352f980fd:/opt/airflow$ cat /home/airflow/.local/lib/python3.12/site-packages/airflow/providers/common/sql/operators/sql.py  |  grep SQLExecuteQueryOperator
  class SQLExecuteQueryOperator(BaseSQLOperator):
  ```

# Extraction des données par API et Transformations

## a. Extraction des données par API

- France Travail (https://francetravail.io/data/api) met à disposition plusieurs APIs, dont "Offres d'emploi v2" (`GET https://api.francetravail.io/partenaire/offresdemploi`).

- Le endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search` permet de récupérer les offres d'emploi actuelles selon plusieurs paramètres dont :

  - le code des appellations ROME pour filtrer par métier (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations`) :

    ```json
    { "code": "38971",  "libelle": "Data analyst" },
    { "code": "38972",  "libelle": "Data scientist" },
    { "code": "404278", "libelle": "Data engineer" },
    { "code": "38975",  "libelle": "Data_Manager" },
    ...
    ```

  - le code des pays (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/pays`) :

    ```json
    { "code": "01", "libelle": "France" },     // inclut les offres en France d'outre-mer et en Corse
    { "code": "02", "libelle": "Allemagne" },  // les pays étrangers ne retournent malheureusement pas d'offres sur les métiers à analyser
    ...
    ```

  - le paramètre `range` qui limite les résultats à 150 offres par requête (avec un status code à `206` si une requête renvoie plus de 150 offres), sachant que l'API ne permet de récupérer que 3150 offres au maximum par appellation ROME.

    - Ainsi, si une requête renvoit 351 offres, il faut enchainer 3 requêtes pour obtenir toutes les offres (la première requête donne les offres `0-149` (status code 206), la deuxième donne les offres `150-299` (status code 206), et la troisième donne les offres `300-350` (status code 200)).


- Cet API nous retourne des offres d'emploi sous forme de documents json avec énormément d'attributs dont l'identifiant de l'offre, son intitulé, sa description, le lieu de travail, des informations sur l'entreprise et sur le contrat, les compétences demandées et l'expérience nécessaires, etc...

- Toutefois, l'API retourne aussi énormément d'offres sans lien avec le métier renseigné en paramètre (par exemple, une requête renseignant l'appellation `Data Engineer` peut renvoyer une offre telle que `Product Owner` car les termes `Data Engineer` peuvent être présents dans la description de l'offre d'emploi).

- On va requêter ainsi un large panel de métiers, dont 29 ayant un lien avec la data, et 32 ayant un lien avec les métiers de la tech (dev, sécurité, devops...), pour maximiser les chances d'obtenir le plus d'offres d'emploi ayant un lien avec les métiers DE, DA et DS, et aussi pour avoir une base de données plus conséquente.

  - En effet, des offres de `Data Engineer` peuvent être présentes en requêtant l'appellation `Data_Manager` par exemple.

- On obtient finalement 61 fichiers json contenant toutes les offres d'emploi liées ou pas à la data, pour la France et DOM-TOM uniquement, l'API de France Travail ne renvoyant quasiment pas d'offre d'emploi pour les autres pays.

  - Ces 61 fichiers json seront concaténés dans un seul fichier json, où les doublons seront supprimés.


- Notes :

  - Les paramètres liés aux dates (`minCreationDate`, `maxCreationDate`, `publieeDepuis`) ne permettent pas d'obtenir des offres expirées (par exemple celles qui ont permis de recruter quelqu'un).

  - Les offres d"emploi retournées peuvent provenir soit de France Travail, soit des `partenaires`, par exemple (`CADREMPLOI`, `DIRECTEMPLOI`, `INDEED`, etc...)


## b. Transformation des données

### Conservation des offres en France Métropolitaine uniquement

- On va dans ce projet se focaliser sur les offres en France Métropolitaine.

  - Pour supprimer les offres en dehors de la métropôle, on se basera sur le numéro du département, qui est à 3 chiffres pour les DOM-TOM, et égales à `2A` ou `2B` pour la Corse.

    - Dans ce cas, on supprimera les offres en DOM-TOM et en Corse avec la regex `^(\d{3}|2(A|B))\s-\s`.

  - L'attribut `libelle` donne l'information lorsque qu'une offre se retrouve dans le `cas_3` (voir partie ci-dessous), c'est-à-dire lorsque `libelle` est de la forme "<département> - <nom_du_département>", par exemple : `971 - Guadeloupe`, `974 - Réunion`, `2A - Corse du Sud`, `2B - BASTIA`.



### Ajout des attributs "nom_ville", "nom_commune", "code_departement", "nom_departement", "code_region", "nom_region"

- Le screenshot suivant (issu du fichier `step_1__location_cases.xlsx`) résume la partie décrite ci-dessous :

  ![cas avec les attributs de localisation](screenshots/location_attributes_cases.png)



- On a dû générer le fichier `api_extract__transform/locations_information/code_name__city_department_region.csv` pour pouvoir catégoriser les cas décrits ci-après, et ainsi récupérer les attributs `nom_ville`, `nom_commune`, `code_departement`, `nom_departement`, `code_region`, `nom_region`.

    - [todo: écrire le .py + préciser le nom du script]

  - Ce fichier csv :
    - a été généré à partir de 4 fichiers récupérés sur le site de l'insee et sur data.gouv :

      - `v_commune_2024.csv`, `v_departement_2024.csv` et `v_region_2024.csv` (https://www.insee.fr/fr/information/7766585)
      - `cities.csv` (https://www.data.gouv.fr/fr/datasets/villes-de-france/)

    - donne le mapping entre :

      - `code_insee` et `nom_commune`
      - `code_postal` et `nom_ville`
      - `code_departement` et `nom_departement`
      - `code_region` et `nom_region`


- Pour les offres récupérées, l'attribut `lieuTravail` peut renseigner les champs suivants `libelle`, `latitude`, `longitude`, `code_postal` et `code_insee`.

  - Ces champs peuvent permettre de retrouver la ville, le département et/ou la région d'une offre d'emploi.

- Dans les cas décrits par la suite, on part du cas le plus favorable au cas le plus défavorable.

- Pour exemple, les cas suivants donneront une idée de pourcentage d'offres pour chacun des cas, à partir du json disponible en archive : "api_extract__transform/outputs/_archives/2025-03-02--exemples-jsons-et-json-concatenated/2025-03-02--18h36__extraction_occurence_1.json", qui contient 13 639 offres.

- Pour catégoriser les offres, on va écrire pour chacune des offres si elle est dans le `cas_1`, dans le `cas_2`, etc... dans une colonne dédiée (`lieu_cas`).


#### Cas_1 : "code_insee" renseigné

- Dans ce cas, on peut récupérer la ville, le département, et la région.

  - Sur le json archivé, c'est le cas pour 12 118 offres sur 13 639, soit 88.85% des offres.

- Notes :
  - dans ce cas, il se peut que `code_postal` ne soit pas renseigné
  - si `code_insee = NAN`, alors `code_postal = NAN` aussi (donc la colonne code_postal n'est pas utile pour retrouver la ville)


##### Ajout des attributs de localisation

- On a donc le code commune.
- A partir du fichier `codes_city_department_region_names.csv`, on ajoute la ville, le département, et la région.


#### Cas_2 : "code_insee = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées

- Dans ce cas, on peut récupérer la ville, le département, et la région.

  - Sur le json archivé, c'est le cas pour 191 offres sur 13 639, soit 1.40% des offres.

- Ici, il y a 2 sous-cas :
  - soit les coordonnées GPS sont corrects,
  - soit la valeur de la latitude et la valeur de la longitude sont inversées.

- On va se baser sur https://fr.wikipedia.org/wiki/Liste_de_points_extr%C3%AAmes_de_la_France pour trouver les variations des coordonnées GPS en France Métropolitaine.

- En effet :
  - le point le plus au nord : (51° 05′ 21″ N, 2° 32′ 43″ E)
  - le point le plus au sud : (42° 19′ 58″ N, 2° 31′ 58″ E)
  - le point le plus à l'est : (48° 58′ 02″ N, 8° 13′ 50″ E)
  - le point le plus à l'ouest : (48° 24′ 46″ N, 4° 47′ 44″ O)


- En convertissant ces coordonnées en valeur décimale, on trouve les fourchettes suivantes pour la latitude et la longitude de la France Métropolitaine :

  - Latitude : 42,3328 (Sud) -> 51,0892 (Nord)
  - Longitude : -4,7956 (Ouest) -> 8,2306 (Est)


- Pour vérifier si la latitude a été inversée avec la longitude :
  - on vérifie si la latitude renseignée est bien comprise entre 42.3328 et 51.0892,
    - si oui, ça correspond à une latitude de la France Métropolitaine,
    - si non, on vérifie que la valeur renseignée pour la longitude l'est bien
      - si oui, on inversera la valeur de la latitude avec la valeur de la longitude.


##### Ajout des attributs de localisation

- La lib geopy permet de retrouver plusieurs informations (`city`, `city_district`, `postcode`, `suburb`, `municipality`, `state`, `town`...), mais tous ces attributs ne sont pas toujours disponibles...
  - En revanche, l'information qui semble toujours être retourné est le code postal.

- A partir du code postal, on ajoute la ville, le département et la région.


- Parfois le code postal retourné par geopy n'est pas présent dans le fichier `code_name__city_department_region.csv` (et donc non présent dans https://www.data.gouv.fr/fr/datasets/villes-de-france/, ni sur https://www.data.gouv.fr/fr/datasets/base-officielle-des-codes-postaux/).

  - Par exemple, sur le json archivé, c'est le cas pour 4 offres où geopy renvoit les codes postaux "34009", "06205", "57045", "13030".

  - Dans ce cas, on va prendre les 2 premiers digits du code postal pour avoir le département, et récupérer la région.


- Notes :

  - C'est assez long (~5 minutes pour 191 offres) car la méthode `geolocator.reverse()` fait une requête http pour chaque offre.

  - Geopy retourne un code postal, mais ce code postal peut être associé à plusieurs villes.
    - Par conséquent, si une offre renseigne le code postal 78310, elle peut être soit à Coignières soit à Maurepas, qui partagent le même code postal, ce qu'on ne peut pas deviner.
    - Cela ne pose pas vraiment problème, étant donné qu'en général plusieurs villes qui ont le même code postal sont relativement proches/voisines.



#### Cas_3 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = 'numéro_département - nom_département'"

- Dans ce cas, on ne peut pas retrouver la ville, mais on peut retrouver le département, et par conséquent la région.

  - Sur le json archivé, c'est le cas pour 804 offres sur 13 639, soit 5.89% des offres.



##### Ajout des attributs de localisation

- Dans ce cas, on a par exemple `libelle = 75 - Paris (Dept.)`, donc on va extraire le code du département dans la colonne `code_departement`, et récupérer `nom_departement`, `code_region` et `nom_region` à partir du fichier `code_name__city_department_region.csv`.



#### Cas_4 : "code_postal = code_insee = latitude = longitude = NAN", mais "libelle = nom_région"

- Dans ce cas, on a que la région, et on ne peut donc pas avoir la ville ni le département.

  - Sur le json archivé, c'est le cas pour 54 offres sur 13 639, soit 0.39% des offres.


- A noter que le nom de la région n'est pas toujours homogène, par exemple, on peut avoir "Ile-de-France" et "Île-de-France" (i avec ou sans accent circonflexe), ce qui est traité dans le script.


##### Ajout des attributs de localisation

Dans ce cas, on écrira `code_region` et `nom_region` à partir du fichier `code_name__city_department_region.csv`.


#### Cas_5 : "code_postal = code_insee = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"

- C'est le cas le plus défavorable qui ne permet pas de retrouver la ville, le département ni la région.

  - Sur le json archivé, c'est le cas pour 252 offres sur 13 639, soit 1.85% des offres.


- On pourrait aller plus loin, et tenter de retrouver l'information dans l'intitulé ou la description de l'offre d'emploi, mais on ne le fera pas ici.


## c. Script "api_extract__transform/extract_and_transform_data.py"

Tout se base dans le dossier `api_extract__transform/outputs/offres/1--generated_json_file`, qui doit contenir zéro fichier json, ou un seul fichier json.

  - S'il y a plusieurs fichiers json dans ce dossier, le script s'arrête.

  - S'il y a aucun fichier json dans ce dossier, le script :

    - 1. supprime tous les fichiers json du dossier `api_extract__transform/outputs/offres/0--original_json_files_from_api`
    - 2. récupère toutes les offres par API (61 fichiers json)
    - 3. concatène les 61 fichiers en 1 fichier json
    - 4. retire de ce fichier toutes les offres qui sont hors de la France métropolitaine
    - 5. ajoute des attributs de localisation `nom_commune`, `nom_ville`, `code_departement`, `nom_departement`, `code_region`, `nom_region` à partir du code insee, des coordonnées GPS et des informations renseignées dans l'attribut `libelle`, comme le département ou la région.
    - 6. ajoute un attribut `dateExtraction` à la date du jour actuelle, qui correspond à la date d'extraction des données par API
    - 7. ajoute un attribut `datePremiereEcriture` à la date du jour actuelle, qui correspond à la date où on écrit une offre dans la base la première fois.

  - S'il y a un fichier json dans ce dossier, le script :
    - supposons que le nom de ce fichier `json_1` soit `2025-04-09--14h19__extraction_occurence_2.json`
    - le script va créer un autre fichier `json_2` à la date/heure du jour et incrémenter l'occurence, le fichier `json_2` s'appellera par exemple `2025-04-12--21h41__extraction_occurence_3.json`
    - les étapes 1-6 précédentes sont exécutées pour `json_2`
    - le script va ensuite concaténer avec "`json_1` - `json_2`" et `json_2` (il y a une intersection entre `json_1` et `json_2`) dans `json_2`
    - l'attribut `datePremiereEcriture` aura la date du jour pour toutes les nouvelles offres, mais prendra les anciennes valeurs pour les anciennes offres
    - `json_1` est déplacé dans le dossier `archive_json_files`, laissant `json_2` être le seul fichier json
       dans le dossier `api_extract__transform/outputs/offres/1--generated_json_file`


Le fichier json servira d'entrée à un autre script `load_sql/2--script_insert_into_tables.py`.

# Chargement des données dans une base de données relationnelle

- L'API de France Travail contient beaucoup d'attibuts pour une offre d'emploi, qui seront quasiment tous exploités par la suite.

  - Seuls les attributs liés aux `contacts` et aux `agences` ne seront pas conservé, n'apportant pas d'utilité.

- Pour la suite, une modélisation snowflake est utilisée :

  ![screenshot du workflow](screenshots/UML.png)

- Le SGBD PostgreSQL sera utilisé, et la base de données sera hébergée dans un conteneur Docker exécutant le service PostgreSQL.

  - PostgreSQL a été choisi pour ses performances, sa fiabilité et sa flexibilité.
  - En tant que solution open source, il offre une grande transparence et une forte extensibilité.
  - Il prend en charge des types de données complexes, respecte les principes ACID et bénéficie d’une communauté active assurant une évolution continue.


- Les données issues du json généré dans la première étape seront récupérées et écrites en base avec la librairie psycopg2.


## Problématiques rencontrées lors de la mise à jour de la base de données après récupération de nouvelles offres

### Evolution de "qualification_code"

- Certaines offres voient la valeur de l'attribut `qualification_code` évoluer, par exemple :

  - `offre_id = 188LLXS` (`intitule = Technicien de gestion de données sur équipement (H/F)`) :
    - lors de `date_extraction = 2025-03-02` : `qualification_code = 7`
    - lors de `date_extraction = 2025-04-05` : `qualification_code = 8`

  - `offre_id = 186XNDD` (`intitule = Coach sportif(ve) (H/F)`) :
    - lors de `date_extraction = 2025-03-02` : `qualification_code = 6`
    - lors de `date_extraction = 2025-04-05` : `qualification_code = 7`


- Avec l'attribut `date_extraction` qui vient de la table `OffreEmploi`, on n'a pas moyen de savoir quelle ligne parmi les suivantes sont les plus récentes, car pour chaque mise à jour, l'attribut `date_extraction` est mis à jour et prend la valeur `2025-04-05`.

  | offre_id | qualification_code | date_extraction |
  | -------- | ------------------ | --------------- |
  | 188LLXS  | 7                  | 2025-04-05      |
  | 188LLXS  | 8                  | 2025-04-05      |
  | 186XNDD  | 6                  | 2025-04-05      |
  | 186XNDD  | 7                  | 2025-04-05      |


- Ce qui nous intéresse est d'avoir la date d'extraction réelle :

  | offre_id | qualification_code | date_extraction |
  | -------- | ------------------ | --------------- |
  | 188LLXS  | 7                  | 2025-03-02      |
  | 188LLXS  | 8                  | 2025-04-05      |
  | 186XNDD  | 6                  | 2025-03-02      |
  | 186XNDD  | 7                  | 2025-04-05      |

pour ne garder que le `qualification_code` le plus récent si 1 offre_id est présente avec 2 qualification_code différents :

  | offre_id | qualification_code | date_extraction |
  | -------- | ------------------ | --------------- |
  | 188LLXS  | 8                  | 2025-04-05      |
  | 186XNDD  | 7                  | 2025-04-05      |


- Il faut donc ajouter `date_extraction` dans la table `offre_qualification`.


### Evolution de "experienceExige" et "experienceLibelle"

Même problématique avec certaines offres qui voient la valeur de l'attribut `experienceExige` et leur `experienceLibelle` évoluer, par exemple :

  - `offre_id = 1316532` (`intitule = Administrateur linux (H/F)`) :

    - lors de `date_extraction = 2025-03-02` : `experienceExige = E` et `experienceLibelle = Expérience exigée de 3 An(s)` (par exemple `experience_id = 6`)

    - lors de `date_extraction = 2025-04-05` : `experienceExige = D` et `experienceLibelle = Débutant accepté` (par exemple `experience_id = 2`)



# Consommation des données

## a. Power BI

### Connexion avec la db

- cf https://learn.microsoft.com/fr-fr/power-query/connectors/postgresql

- `Blank report`

- `Get data` > `PostgreSQL database` > `connect`

  - fenêtre `PostgreSQL database` :
    - `Server : localhost`
    - `Database : francetravail`
    - `Data Connectivity mode : Import`
      - Notes :
        - Import → Charge toutes les données en mémoire de Power BI.
        - DirectQuery → Interroge PostgreSQL en temps réel sans stocker les données localement.
    - `Advanced options` : pas touché

  - fenêtre `localhost;francetravail` :
    - `User name : mhh`
    - `Password : mhh`
    - `Select which level to apply these settings to : localhost`


  - fenêtre `Encryption Support` :

    - `We were unable to connect to the data source using an encrypted connection. To access this data source using an unencrypted connection, click OK.` => On valide.

  - fenêtre `Navigator`, où on peut sélectionner les 19 tables.

    - On sélectionne tout, puis `Load`.

      - fenêtre `Processing Queries` (Determining automatic transformations...)

        - On peut `Skip`, ce qu'on va faire après une dizaine de minutes, car ça bloque sur la table `formation` (pourtant, toutes les autres tables sont bien validées, et on arrive bien à voir le contenu de la table `formation` par une requête sql)

        - Note : on n'a pas cette fenêtre la deuxième fois (Power BI avait crashé quand j'ai voulu sauvegardé la première fois)

          - fenêtre `Load` (qui finit par bien aboutir)


### Model view

- Onglet `model view` : on voit bien les 19 tables, on doit refaire les liens créés automatiquement.

  - On procède comme le diagramme UML qu'on a défini (voir `load_sql/UML.drawio`)


- On masque les colonnes non utilisées.

- Paramétrer `Cross-filter direction = Both` pour certains liens est nécessaire pour la data viz.



### Table view

- Création table de date

- Création de colonnes :
  - Date Différence = DATEDIFF('Offre Emploi'[Date Création], 'Offre Emploi'[Date Actualisation], DAY)


### Transformations sur Power BI

#### Renommage de toutes les colonnes

- C'est juste pour Power BI.

- On renomme les colonnes avoir des noms plus facile à lire dans les rapports comme :

  - `Offre ID` (au lieu de `offre_id`)
  - `Durée Travail Libellé` (au lieu de `duree_travail_libelle`)


#### Attribut "Liste Mots-Clés"

- Exemple de valeur pour une offre : `{etl,git,"power bi",python,sql,tableau}`

- On supprime les accolades et les guillemets.
  - ce qui donne pour l'exemple : `etl,git,power bi,python,sql,tableau`

- On éclate la colonne en faisant `Split Column` > `By delimiter` (Split into Rows)
  - l'offre est donc splittée sur 6 lignes avec un seul mot-clé dans la colonne `Liste Mots Clés`


#### Ajout de variables avec le nom des villes, départements et région modifiés pour la data viz

##### Ajout de la variable "Nom Ville Modifié"

- Dans le `report view` / carte mondiale, on a des villes françaises qui sont situées dans d'autres pays, par exemple :

  - offre_id = `2083056` dans la ville `Cologne` (code postal 32 430) en région Occitanie, département Gers  => placé en Allemagne (NOK, car on est censé avoir que des offres en France)

    ![Cologne en Allemagne](screenshots/power_bi/city_Cologne_in_Germany.png)


  - offre_id = `2757953` dans la ville `La Réunion` (code postal 47 700) en région Nouvelle-Aquitaine, département Lot-et-Garonne  => placé en France (OK)

    ![Cologne en France](screenshots/power_bi/city_Cologne_in_France.png)


- Comme vu dans le dernier screenshot, pour avoir les villes placées en France, on définit une colonne `Nom Ville Modifié` avec le nom de la ville suffixé avec `, France` (par exemple `Cologne, France`).


##### Ajout de la variable "Nom Département Modifié"

Même chose pour le département de la `Lot` qui est placé en Lituanie, on ajoute une colonne qui suffixera le nom du département avec `, France` :

  - Département `Lot` en Lituanie :

    ![Département "Lot" en Lituanie](screenshots/power_bi/department_Lot_in_Lithuania.png)


  - Département `Lot` en France :

    ![Département "Lot" en France](screenshots/power_bi/department_Lot_in_France.png)


##### Ajout de la variable "Nom Région Modifié"

- Quand on affiche la carte du monde avec les régions de la France, on constate que 2 régions (la Bretagne et l'Occitanie) ne sont pas complètement coloriées comme les autres régions :

  - pour la Bretagne :

    ![Bretagne non colorié entièrement](screenshots/power_bi/region_Bretagne_KO.png)


  - pour l'Occitanie :

    ![Occitanie non colorié entièrement](screenshots/power_bi/region_Occitanie_KO.png)


- Changer le `Data category` (à `County` ou `State or Province`) résout le problème pour l'Occitanie mais pas la Bretagne.

- Le contournement est d'ajouter une colonne, où on préfixera le nom de la région de `Région d('|de|du|des)` en fonction des régions, par exemple :

  - `Région d'Île-de-France`
  - `Région de Normandie`
  - `Région des Hauts-de-France`
  - `Région du Grand Est`

- A noter qu'il y a une exception pour `Région Bourgogne-Franche-Comté` (pas de `de`).

- Cela résout bien le problème de colorisation :

  - pour la Bretagne :

    ![Bretagne colorié entièrement](screenshots/power_bi/region_Bretagne_OK.png)

  - pour l'Occitanie :

    ![Occitanie colorié entièrement](screenshots/power_bi/region_Occitanie_OK.png)



## b. Requêtes SQL

### Transformations pour écrire l'attribut "metier_data"

- Pour identifier les offres de "Data Engineer" parmi toutes les offres récupérées, le premier réflexe serait de filtrer sur le rome_code `M1811` qui correspond à `Data engineer`, mais on se rend compte que les offres d'emploi associées ne sont pas toutes liées à ce poste.

- On retrouve en effet des postes d'architecte, d'ingénieur base de données, de data analyst, de data manager, de technicien data center, etc... (voir résultats de la requête `sql_requests/1_requests/offers_DE_DA_DS/10--table_descriptionoffre__rome_M1811.pgsql`)  # chemin à modifier

- L'attribut `intitule_offre` de la table `DescriptionOffre` sera donc utilisé pour filtrer les offres voulues (ici : `Data Engineer`, `Data Analyst` et `Data Scientist`) grâce à des requêtes qui utilisent des regex, écrivant la valeur `DE`, `DA`, `DS` dans l'attribut `metier_data` (voir `sql_requests/0_transformations`).



### Transformations pour écrire les attributs "salaire_min" et "salaire_max"

#### Contexte

- Pour écrire ces attributs qui donnent les salaires minimum et maximum annuels, on se base sur l'attribut `salaire_libelle`, qui n'est pas toujours renseigné.

- Lorsqu'elle l'est, les valeurs pour cet attribut sont parfois mal renseignées par les recruteurs :

  - qui inversent parfois le salaire annuel avec le salaire mensuel [auquel cas on fera un traitement (voir ci-dessous) pour avoir les bons salaires] :

    - `Annuel de 486,00 Euros à 1801,00 Euros` (c'est sûrement un salaire mensuel et non annuel)
    - `Mensuel de 32000,00 Euros à 40000,00 Euros` (c'est sûrement un salaire annuel et non mensuel)

  - qui inversent les salaires min et max [auquel cas on les inversera] :

    - `Annuel de 60000,00 Euros à 40000,00 Euros`

  - qui se trompent sûrement dans les salaires renseignés :

    - `Autre de 30000,00 Euros à 400000,00 Euros` (salaire max = 400k : sûrement erroné avec un 0 en trop)
    - `Annuel de 80000,00 Euros à 850000,00 Euros` (idem avec salaire max = 850k)
    - `Annuel de 550000.0 Euros sur 12.0 mois` (salaire = 550k : sûrement erroné avec un 0 en trop)


- D'autre part, il faut noter que beaucoup d'offres ne renseignent que le taux horaire [auquel cas on écrira null], par exemple :

  - `Annuel de 11,00 Euros` (c'est sûrement un taux horaire)
  - `Horaire de 11.88 Euros sur 12 mois`


#### Hypothèses

- Comme on n'est pas certain si les salaires indiqués sont mensuels ou annuels (à cause des erreurs des recruteurs), on va prendre les hypothèses suivantes :
  - salaire mensuel ∈ [1 666, 12 500]
  - salaire annuel ∈ [20 000, 150 000]

- Donc, on considère que si salaire mensuel :
  - inférieur à 1666 € (20k), ce n'est pas un salaire mensuel (pour écarter les taux horaires, les salaires à mi-temps, les salaires en alternance...)
  - supérieur à 12 500 € (150k), c'est très certainement une faute de frappe (il y a vraiment très peu d'offres dans ce cas, peut-être 4 pour 13k offres)

    - par exemple :

      - Ingénieur systèmes embarqués (H/F) : `Annuel de 80000,00 Euros à 850000,00 Euros` (80k - 850k)
      - Administrateur Bases de données - DBA / Microsoft SQL Server(H/F) (H/F)	: `Mensuel de 400000.0 Euros à 450000.0 Euros sur 12.0 mois` (400k - 450k)
	    - Chef de Projet EDI (H/F) : `Annuel de 50000.0 Euros à 540000.0 Euros sur 12.0 mois` (50k - 540k)
      - Data Analyst H/F: `Annuel de 45000,00 Euros à 550000,00 Euros` (45k - 550k)


#### Algorithme

- Pour les transformations, on va considérer les cas suivants.

- Si "salaire_libelle" donne :

  - A. une fourchette de salaire ("cas fourchette") :

    - `Annuel de 60000.0 Euros à 90000.0 Euros`
    - `Annuel de 60000.0 Euros à 90000.0 Euros sur 12.0 mois`
    - `Annuel de 60000.0 Euros à 90000.0 Euros sur 13.0 mois`
    - `Mensuel de 1767.00 Euros à 2600.00 Euros sur 12 mois`
    - `Mensuel de 1767.00 Euros à 2600.00 Euros`
    - `Autre de 1910,00 Euros à 2050,00 Euros`
    - `De 40000,00 Euros à 40000,00 Euros`
    - `Autre de 40000,00 Euros à 45000,00 Euros`
    - `Cachet de 50000,00 Euros à 55000,00 Euros`


      - cas 1 : Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [1 666 €, 12 500 €] (on considère que c'est un salaire mensuel)
        - alors on inverse les salaires mensuels minimum et maximum.

          - exemple :
            - `Mensuel de 5500.0 Euros à 4200.0 Euros sur 12.0 mois`


      - cas 2 : Si salaires min+max récupérés ∈ [1 666 €, 12 500 €] (on considère que c'est un salaire mensuel)
        - alors on récupère les salaires minimum et maximum et on les multiplie par 12.

          - exemples :
            - `Annuel de 1800,00 Euros à 2000,00 Euros`
            - `Mensuel de 2900,00 Euros à 3000,00 Euros`
            - `Autre de 1855,26 Euros à 1855,26 Euros`


      - cas 3 : Si salaire minimum récupéré > salaire maximal récupéré *ET* salaires min+max récupérés ∈ [20 000 €, 150 000 €] (on considère que c'est un salaire annuel)
        - alors on inverse les salaires annuels minimum et maximum.

          - exemple :
            - `Annuel de 60000,00 Euros à 40000,00 Euros`


      - cas 4 : Si salaires min+max récupérés ∈ [20 000 €, 150 000 €] (on considère que c'est un salaire annuel)
        - alors on récupère les salaires minimum et maximum.

          - exemples :
            - `Annuel de 55000,00 Euros à 65000,00 Euros`
            - `Mensuel de 45000.0 Euros à 50000.0 Euros sur 12.0 mois`
            - `Autre de 45000,00 Euros à 55000,00 Euros`


      - cas 5 : Sinon, dans les autres cas
          - alors salaire min/max = NULL.

            - exemples où `salaire minimum <= 1 666 €` :
              - `Annuel de 25,00 Euros à 30,00 Euros`
              - `Mensuel de 850,00 Euros à 950,00 Euros`
              - `De 13,00 Euros à 14,00 Euros`

            - exemples où `salaire max >= 150 000 €` :
              - `Annuel de 80000,00 Euros à 850000,00 Euros`
              - `Mensuel de 400000.0 Euros à 450000.0 Euros sur 12.0 mois`
              - `Autre de 30000,00 Euros à 400000,00 Euros`

            - exemple où `salaire n'appartient pas aux fourchettes de salaires mensuels [1 666, 12 500] ni annuels [20 000, 150 000]` :

              - `Annuel de 19000,00 Euros à 19000,00 Euros`



  - B. un salaire unique ("cas salaire unique") :

    - `Annuel de 48000.0 Euros sur 12.0 mois`
    - `Annuel de 50000,00 Euros`
    - `Mensuel de 45000.0 Euros sur 12.0 mois`


      - cas 2 : Si salaire récupéré ∈ [1 666 €, 12 500 €] (on considère que c'est un salaire mensuel)
        - alors on récupère le salaire et on le multiplie par 12.

          - exemples :
            - `Mensuel de 4410,00 Euros`


      - cas 4 : Si salaire récupéré ∈ [20 000 €, 150 000 €] (on considère que c'est un salaire annuel)
        - alors on récupère le salaire.

          - exemples :
            - `Annuel de 55000.0 Euros sur 12.0 mois`


      - cas 5 : Sinon, dans les autres cas
        - alors salaire min/max = NULL.

          - exemples :
            - `Annuel de 1000,00 Euros`
            - `Mensuel de 12,00 Euros`
            - `Annuel de 550000.0 Euros sur 12.0 mois`



#### Exemples d'offres réelles avec les salaires qu'on fixe


| offre_id | intitule_offre                         | salaire_libelle                              | get_salaire_min | get_salaire_max | cas                | sous-cas                                    | salaire_min | salaire_max |
| -------- | -------------------------------------- | -------------------------------------------- | --------------- | --------------- | ------------------ | ------------------------------------------- | ----------- | ----------- |
| -        | -                                      | -                                            | -               | -               | -                  | 1 (min>max + mois ∈ [1 666, 12 500])        | -           | -           |
| 2430874  | Chef de projet (H/F)                   | Mensuel de 5880,00 Euros à 8085,00 Euros     | 5880            | 8085            | cas fourchette     | 2 (mois ∈ [1 666, 12 500])                  | 70560       | 97020       |
| 188TYKG  | MANAGEUR-EUSE DE TRANSITION (H/F)      | Mensuel de 3136.0 Euros sur 12.0 mois        | 3136            | 12              | cas salaire unique | 2 (mois ∈ [1 666, 12 500])                  | 37632       | 37632       |
| 2861769  | Chef de projet (H/F)                   | Annuel de 60000,00 Euros à 40000,00 Euros    | 60000           | 40000           | cas fourchette     | 3 (min>max + an ∈ [20 000, 150 000])        | 40000       | 60000       |
| 2710913  | Responsable BI / Data (H/F)            | Annuel de 75000,00 Euros à 90000,00 Euros    | 75000           | 90000           | cas fourchette     | 4 (an ∈ [20 000, 150 000])                  | 75000       | 90000       |
| 188LKVH  | Technicien d'exploitation informatique | Annuel de 25200.0 Euros sur 12.0 mois        | 25200           | 12              | cas salaire unique | 4 (an ∈ [20 000, 150 000])                  | 25200       | 25200       |
| 6071688  | Management de Projets Numériques H/F   | Mensuel de 850,00 Euros à 950,00 Euros       | 850             | 950             | cas fourchette     | 5 (autres cas : salaire < 1666 €)           | null        | null        |
| 2554957  | Chef de Projet Eds Entrepôt de Données | Annuel de 19000,00 Euros à 19000,00 Euros    | 19000           | 19000           | cas fourchette     | 5 (autres cas : salaire ∈ ]12 500, 20 000[) | null        | null        |
| 2968347  | Gestionnaire ERP (H/F)                 | Mensuel de 352800,00 Euros à 411600,00 Euros | 352800          | 411600          | cas fourchette     | 5 (autres cas : salaire > 150 000 €)        | null        | null        |


- A noter aussi que les salaires des offres en alternance seront exclues ici car leur salaire est très majoritairement inférieur au seuil minimum qu'on a défini ici.


### Analyse du jeu de données à travers des requêtes SQL

- voir le dossier `sql_requests/1_requests/offers_DE_DA_DS/`

- Au moins une requête sera faite pour chaque table de dimension pour mieux comprendre notre jeu de données.


# Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL

## a. Création d'une API pour la db

- Utilisation de `FastAPI`.

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.


## b. Dockerisation de l'application et de la db PostGreSQL

- Arborescence avec les éléments importants liés à la dockerisation :

  .
  ├── api_extract__transform
  │   ├── locations_information
  │   │   ├── code_name__city_department_region.csv   # fichier utilisé par le script fastapi
  │  
  ├── fastapi/                                        # application FastAPI
  │   ├── Dockerfile                                  # construction du conteneur FastAPI
  │   ├── locations_information                       # point de montage (volume)  # todo : à renommer en "locations_information_mount" ?
  │   ├── main.py                                     # script fastapi
  │   ├── requirements.txt                            # dépendances pour pouvoir lancer le script fastapi dans le conteneur
  │   └── sql_requests                                # requêtes SQL utilisées par le script fastapi
  │  
  ├── docker-compose.yml                              # orchestration docker pour postgres + fastapi



- Travail en mode "dev" :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]` (avec l'option `--reload` pour ne pas avoir à relancer la commande après une modification)
  - `docker-compose.yml` :
    - avec les montages de volumes pour ne pas avoir à relancer le docker-compose après chaque modification de fichiers sql

- passage en mode "prod" quand les devs sont terminés :
  - `Dockerfile` :
    - `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` (sans l'option `--reload`)
    - `COPY` du script python, et des fichiers nécessaires dans le conteneur (fichier csv, fichiers sql), au lieu de passer par des volumes


# Ce qu'on avait avant les travaux et ce qu'il faut modifier


## Ce qu'on avait avant les travaux

La moulinette Python crée les fichiers suivants dans le dossier "api_extract__transform/outputs/offres" :

  - `concatenate_all_json_into_one()` :
        => json_generated_filename_0 = "2025-03-05--22h09__0__all__13639_offres.json"

  - `add_date_extract_attribute()` :
        => json_generated_filename_1 = "2025-03-05--22h09__1__all__13639_offres__with_date_extraction_attribute.json"

  - `keep_only_offres_from_metropole()` :
        => json_generated_filename_2 = "2025-03-05--22h09__2__only_metropole__13419_offres.json"

  - `add_location_attributes()` :
        => json_generated_filename_3 = "2025-03-05--22h09__3__with_location_attributes.json"


## Ce qu'il faut modifier

- Il n'est pas nécessaire d'avoir les fichiers json intermédiaires, donc chaque méthode écrasera le fichier qu'il a en entrée.

- Optimisation du temps d'exécution :

  - Les fonctions `add_date_extract_attribute()` et `keep_only_offres_from_metropole()` ne prennent que quelques secondes d'exécution.
  - Par contre, `add_location_attributes()` prend 3-5 minutes.
    - Pour éviter de refaire le travail de recherche de localisation pour chaque offre d'emploi, on créera l'attribut `offre_localise` (offre localisé), un booléen qui vaudra `False` si `add_location_attributes()` n'a pas traité l'offre d'emploi.

- Comment savoir si le script a déjà été exécuté ?

  - Si un fichier json n'existe pas dans `api_extract__transform/outputs/offres/1--generated_json_file` :

    - cela signifie que le script n'a jamais été exécuté


  - Si un fichier json existe déjà dans `api_extract__transform/outputs/offres/1--generated_json_file` :

    - cela signifie que le script a déjà été exécuté

    - on connait le nombre d'occurence :
      - si le fichier s'appelle "2025-04-02--14h40__extraction__occurence_1.json", cela signifie qu'il n'y a eu qu'une seule occurence
      - si le fichier s'appelle "2025-04-04--21h14__extraction__occurence_5.json", cela signifie qu'il y a eu 5 occurences
    - le script `extract_and_transform_data.py` doit lorsqu'il est lancé :
      - vérifier l'absence ou la présence d'un fichier json dans `api_extract__transform/outputs/offres/1--generated_json_file` (ce dossier ne contient soit pas de json, soit qu'un seul (pas plusieurs, comme le mentionne le fichier dans ce dossier qui se nomme `_this_folder_should_contain_0_or_1_json_file_`)) :

        - s'il y a un fichier json, le script `extract_and_transform_data.py` devrait mettre à jour la date et l'heure avec le moment où il est lancé, par exemple  "2025-04-02--20h40__extraction__occurence_2.json", le point important est d'avoir "__extraction__occurence_2.json" qui montre que le numéro dans le nom du fichier a été incrémenter

          - l'ancien fichier devra être archivé dans un dossier à part, avant d'être renommé et traité

        - s'il n'y a pas de fichier json, le script `extract_and_transform_data.py` devrait créer un fichier json, par exemple  "2025-04-02--14h40__extraction__occurence_1.json", le point important est d'avoir "__extraction__occurence_1.json" qui mentionne qu'il s'agit de la première occurence

        - s'il contient plusieurs fichiers json, on arrête le script.



# todo : Mise à jour de la base avec les nouvelles données

- A la première exécution, on obtient une base de données avec notamment les attributs `offre_id` et `date_extraction = date_0` (date du jour où la première extraction a lieu).


- Tous les x jours, le process entier devra être ré-exécuté, et devra traiter les cas suivants, par exemple, à `date_1` qui correspond à une date postérieure à `date_0` :

  - Si une offre n'est plus disponible :

    - on ne supprime pas l'offre de la base
    - on laisse `date_extraction = date_0`
    - `to_process = False`


  - Si une offre est toujours disponible :

    - on ne supprime pas l'offre de la base
    - on met à jour `date_extraction = date_1`
    - on met à jour `date_actualisation` avec la nouvelle valeur
    - `to_process = False`


  - Si une offre est nouvelle :

    - on ajoute l'offre dans la base
    - on écrit `date_extraction = date_1`
    - `to_process = True`


- Le nouvel attribut `to_process` (booléen) servira à savoir si une offre doit repasser dans la "moulinette". En effet, une nouvelle offre devra subir les transformations suivantes :

  - Transformations côté Python :

    - Vérifier si la nouvelle offre est en France Métropolitaine (la conserver dans le cas positif, la rejeter sinon)

    - Ajout d'attributs nom/code des villes, communes, départements, régions à partir du code insee, coordonnées GPS, et autres informations


  - Transformations côté SQL :

    - Ajout d'un attribut pour savoir si une offre est pour un DA, un DE ou un DS

    - Ajout des attributs "salaire_min" et "salaire_max"