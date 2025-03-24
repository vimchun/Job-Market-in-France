[Retour à la page principale](../README.md)

# Étape 3 : Consommation des données

## Requêtes SQL

### Transformations pour écrire l'attribut "metier_data"

- Pour identifier les offres de "Data Engineer" parmi toutes les offres récupérées, le premier réflexe serait de filtrer sur le rome_code "M1811" qui correspond à "Data engineer", mais on se rend compte que les offres d'emploi associées ne sont pas toutes liées à ce poste.

- On retrouve en effet des postes d'architecte, d'ingénieur base de données, de data analyst, de data manager, de technicien data center, etc...

  (voir résultats de la requête "sql_requests/1_requests/offers_DE_DA_DS/10--table_descriptionoffre__rome_M1811.pgsql")

- L'attribut "intitule_offre" de la table "DescriptionOffre" sera donc utilisé pour filtrer les offres voulues (ici : "Data Engineer", "Data Analyst" et "Data Scientist") grâce à des requêtes qui utilisent des regex, écrivant la valeur "DE", "DA", "DS" dans l'attribut "metier_data" (voir "sql_requests/0_transformations").


### Analyse du jeu de données à travers des requêtes SQL

- voir le dossier "sql_requests/1_requests/offers_DE_DA_DS/"

- Au moins une requête sera faite pour chaque table de dimension pour mieux comprendre notre jeu de données.


## Power BI