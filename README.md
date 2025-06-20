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

  - [1. Extraction des données par API et Transformations](readme_pages/step_1__extract_and_transform_data.md)

  - [2. Chargement des données dans une base de données relationnelle](readme_pages/step_2__load_data_to_database.md)

  - [3. Consommation des données](readme_pages/step_3__data_consumption.md)

  - [4. Création d'une API pour la db, dockerisation de cette application et de la db PostGreSQL](readme_pages/step_4__api.md)

  - [5. Orchestration avec Airflow](readme_pages/step_5__airflow_orchestration.md)

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


  ![airflow_edit_connection](readme_pages/screenshots/airflow_gui_edit_connection.png)


## Arborescence du projet

todo : à remplir avec commentaires


# Workflow du projet avec Airflow

## Avant Airflow

Avant d'appliquer Airflow au projet, j'avais 2 scripts python.
Pour résumer et simplifier ce qu'il faisait ("simplifier" ici car ces scripts ont été remplacés par des DAGs qu'on détaillera après) :
  - le premier récupérait les données de France Travail, faisait des transformations, et chargeait les offres d'emploi dans un json
  - le second crée lit le json puis écrit les offres d'emploi dans la base de données, et effectue un deuxième lot de transformations à partir de fichier sql.

  ![screenshot du workflow](readme_pages/screenshots/workflow.png)


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
