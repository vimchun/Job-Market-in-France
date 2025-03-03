[Retour à la page principale](../README.md)

# Étape 2 : Récolte des données par API

- L'API de France Travail contient beaucoup d'attibuts pour une offre d'emploi, qui seront quasiment tous exploités par la suite.
  - Seuls les attributs liés aux "contacts" et aux "agences" ne seront pas conservé, n'apportant pas d'utilité.

- Pour la suite, une modélisation snowflake est utilisée :

  ![screenshot du workflow](screenshots/UML.png)


- Le SGBD PostgreSQL sera utilisé, et la base de données sera hébergée dans un conteneur Docker exécutant le service PostgreSQL.

- Les données issues du json généré dans la première étape seront récupérées et écrites en base avec la librairie psycopg2.

