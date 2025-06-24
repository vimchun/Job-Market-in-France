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


Dans l'idéal, il aurait fallu créer cette connexion de manière "encore plus automatique" avec une tâche dans le DAG (cela permettra de ne pas avoir à exécuter le script précédent), mais certaines problématiques nous en empêchent. Ceci est documenté ![ici](readme_files/README_additional_notes.md#création-automatique-de-connexion-postgres)


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


## Description des DAGs

### DAG 1

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


### DAG 2



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

- Plusieurs transformations seront effectuées par la suite : [voir ici](##transformations-des-données-en-amont-côté-python)


- Notes :

  - Les paramètres liés aux dates (`minCreationDate`, `maxCreationDate`, `publieeDepuis`) ne permettent pas d'obtenir des offres expirées (par exemple celles qui ont permis de recruter quelqu'un).

  - Les offres d'emploi retournées peuvent provenir soit de `FRANCE TRAVAIL`, soit des `partenaires` (par exemple `CADREMPLOI`, `DIRECTEMPLOI`, `INDEED`, etc...)


# Transformations des données

## Transformations des données en amont (côté Python)

Plusieurs transformations faites en amont du chargement dans la base Postgres sont effectuées avec Python :

  - Concaténation des 61 fichiers json dans un seul fichier json, avec suppression des doublons
  - Conservation des offres en France Métropolitaine uniquement
    (todo : lien)
  - Ajout des attributs de localisation des offres (noms et codes des villes, départements, départements et régions)
    (todo : lien)
  - Ajout des attributs `date_premiere_ecriture` et `date_extraction`

    - `date_extraction` aura la date du jour à laquelle le DAG 1 a été lancé,
    - `date_premiere_ecriture` aura la date du jour pour toutes les nouvelles offres, mais prendra les anciennes valeurs pour les anciennes offres.



## Transformations des données en aval (côté SQL)


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

- Les données issues du json généré avec le DAG 1 seront récupérées et écrites en base avec la librairie `psycopg2`.


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

Le lien suivant montre comment connecter Power BI à la session Postgres : ![section](readme_files/README_additional_notes.md###connexion_avec_la_db)

Faire de même pour les autres sections...


## Requêtes SQL

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


# Création d'une API pour la db

- Utilisation de `FastAPI`.

- Pour les réponses, on utilisera la librairie `tabulate` avec `media_type="text/plain"` pour afficher un tableau qui facilitera la lecture, et qui diminuera le nombre de lignes des réponses.


