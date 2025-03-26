[Retour à la page principale](../README.md)

# Étape 3 : Consommation des données

## Requêtes SQL

### Transformations pour écrire l'attribut "metier_data"

- Pour identifier les offres de "Data Engineer" parmi toutes les offres récupérées, le premier réflexe serait de filtrer sur le rome_code "M1811" qui correspond à "Data engineer", mais on se rend compte que les offres d'emploi associées ne sont pas toutes liées à ce poste.

- On retrouve en effet des postes d'architecte, d'ingénieur base de données, de data analyst, de data manager, de technicien data center, etc...

  (voir résultats de la requête "sql_requests/1_requests/offers_DE_DA_DS/10--table_descriptionoffre__rome_M1811.pgsql")

- L'attribut "intitule_offre" de la table "DescriptionOffre" sera donc utilisé pour filtrer les offres voulues (ici : "Data Engineer", "Data Analyst" et "Data Scientist") grâce à des requêtes qui utilisent des regex, écrivant la valeur "DE", "DA", "DS" dans l'attribut "metier_data" (voir "sql_requests/0_transformations").

### Transformations pour écrire les attributs "salaire_min" et "salaire_max"

Pour écrire ces attributs qui donnent les salaires minimum et maximum annuels, on se base sur l'attribut "salaire_libelle", qui n'est pas toujours renseigné.

D'abord, il faut noter que beaucoup d'offres ne renseignent pas que le taux horaire, par exemple :

  - `Horaire de 11.88 Euros sur 12 mois`

  On ne récupérera pas les salaires min et max pour ces offres là.


Ensuite, beaucoup d'offres ne renseignent pas les salaires de manière cohérente, par exemple :
  - `Annuel de 486,00 Euros à 1801,00 Euros` (c'est sûrement un salaire mensuel et non annuel)
  - `Annuel de 11,00 Euros` (c'est sûrement un taux horaire)
  - `Mensuel de 32000,00 Euros à 40000,00 Euros` (c'est sûrement un salaire annuel et non mensuel)


Comme on a initialement filtré sur les métiers de la tech (même si l'API renvoie des offres hors de la tech), on va mettre salaire_min et salaire_max à NULL si le salaire minimum est en-dessous de 20 000 € annuelle exclut (on doit forcément choisir une valeur car pour un salaire donné, on ne sait pas si c'est un salaire mensuel ou annuel).

Par conséquent, si le salaire annuel récupéré est strictement inférieur à 20 000 €, on va considérer qu'il s'agit d'un salaire mensuel et on va donc le multiplier par 12.


Pour les transformations, on va considérer les cas suivants.

Si "salaire_libelle" donne :

  - une fourchette de salaire annuelle ("cas 11 (annuel fourchette)") :

    - `Annuel de 60000.0 Euros à 90000.0 Euros`
    - `Annuel de 60000.0 Euros à 90000.0 Euros sur 12.0 mois`
    - `Annuel de 60000.0 Euros à 90000.0 Euros sur 13.0 mois`

      - Si salaire minimale annuel récupéré < 20000/12 (1666.66€) [on suppose que ce n'est pas un salaire mensuel], alors on écrit NULL
        - exemple : `Annuel de 25,00 Euros à 30,00 Euros`

      - Si salaire minimale annuel récupéré compris entre 20000/12 (1666.66€) et 20000 € [on considère que c'est un salaire mensuel], alors on récupère les salaires minimum et maximum et on les multiplie par 12
        - exemple : `Annuel de 1800,00 Euros à 2000,00 Euros`

      - Si salaire minimale annuel récupéré > 20000 € [on considère que c'est un salaire annuel], alors on récupère simplement les salaires minimum et maximum
        - exemple : `Annuel de 55000,00 Euros à 65000,00 Euros`



  - un salaire unique annuel ("cas 12 (annuel salaire unique)") :

    - `Annuel de 48000.0 Euros sur 12.0 mois`
    - `Annuel de 50000,00 Euros`

      - Si salaire annuel récupéré < 20000/12 (1666.66€) [on suppose que ce n'est pas un salaire mensuel], alors on écrit NULL
        - exemple : `Annuel de 40,00 Euros`

      - Si salaire annuel récupéré compris entre 20000/12 (1666.66€) et 20000 € [on considère que c'est un salaire mensuel], alors on récupère les salaires minimum et maximum et on les multiplie par 12
        - exemple factice (cas non rencontré) : `Annuel de 1800,00 Euros`

      - Si salaire annuel récupéré > 20000 € [on considère que c'est un salaire annuel], alors on récupère simplement les salaires minimum et maximum
        - exemple : `Annuel de 55000.0 Euros sur 12.0 mois`

          - `Annuel de 1000,00 Euros`

  - une fourchette de salaire mensuel ("cas 21 (mensuel fourchette)") :

    - `Mensuel de 1767.00 Euros à 2600.00 Euros sur 12 mois`
    - `Mensuel de 1767.00 Euros à 2600.00 Euros`

      - Si salaire minimale mensuel récupéré < 20000/12 (1666.66€) [on suppose que ce n'est pas un salaire mensuel], alors on écrit NULL
        - exemple : `Mensuel de 850,00 Euros à 950,00 Euros`

      - Si salaire minimale mensuel récupéré compris entre 20000/12 (1666.66€) et 20000 € [on considère que c'est un salaire mensuel], alors on récupère les salaires minimum et maximum et on les multiplie par 12
        - exemple : `Mensuel de 2900,00 Euros à 3000,00 Euros`

      - Si salaire minimale mensuel récupéré > 20000 € [on considère que c'est un salaire annuel], alors on récupère simplement les salaires minimum et maximum
        - exemple : `Mensuel de 45000.0 Euros à 50000.0 Euros sur 12.0 mois`


  - un salaire unique mensuel ("cas 22 (mensuel salaire unique)") :

    - `Mensuel de 45000.0 Euros sur 12.0 mois`

      - Si salaire mensuel récupéré < 20000/12 (1666.66€) [on suppose que ce n'est pas un salaire mensuel], alors on écrit NULL
        - exemple : `Mensuel de 12,00 Euros`

      - Si salaire mensuel récupéré compris entre 20000/12 (1666.66€) et 20000 € [on considère que c'est un salaire mensuel], alors on récupère le salaire et on le multiplie par 12
        - exemple : `Mensuel de 800.0 Euros sur 12.0 mois`

      - Si salaire mensuel récupéré > 20000 € [on considère que c'est un salaire annuel] , alors on récupère simplement la valeur
        - exemple : `Mensuel de 55000.0 Euros sur 12.0 mois`


  - une fourchette de salaire mensuelle ou annuelle ("cas 31 (fourchette mensuelle ou annuelle ?)") :
    - `Autre de 1910,00 Euros à 2050,00 Euros`
    - `De 40000,00 Euros à 40000,00 Euros`
    - `Autre de 40000,00 Euros à 45000,00 Euros`
    - `Cachet de 50000,00 Euros à 55000,00 Euros`

      - Si salaire minimale récupéré < 20000/12 (1666.66€) [on suppose que ce n'est pas un salaire mensuel], alors on écrit NULL
        - exemple : `De 13,00 Euros à 14,00 Euros`

      - Si salaire minimale récupéré compris entre 20000/12 (1666.66€) et 20000 € [c'est certainement un salaire mensuel], alors on récupère les salaires minimum et maximum et on les multiplie par 12
        - exemple : `Autre de 1855,26 Euros à 1855,26 Euros`

      - Si salaire minimale > 20000 € [on considère que c'est un salaire annuel], alors on récupère simplement les salaires minimum et maximum
        - exemple : `Autre de 30000,00 Euros à 400000,00 Euros`


Pour finir, voilà un tableau récapitulatif avec ce qu'on écrit dans salaire_min et salaire_max pour les 5 cas décrits précédemment :


  | salaire_libelle                                        | cas                             | salaire_min | salaire_max | commentaire                                                                      |
  | ------------------------------------------------------ | ------------------------------- | ----------- | ----------- | -------------------------------------------------------------------------------- |
  | Annuel de 60,00 Euros à 70,00 Euros                    | cas 11 (annuel fourchette)      | null        | null        | salaire minimum récupéré < 1666 € => on écrit NULL                               |
  | Annuel de 2100,00 Euros à 2200,00 Euros                | cas 11 (annuel fourchette)      | 25200       | 26400       | salaire minimum récupéré compris entre 1666 € et 20 000 € => on multiplie par 12 |
  | Annuel de 40000.0 Euros à 50000.0 Euros sur 12.0 mois  | cas 11 (annuel fourchette)      | 40000       | 50000       | salaire minimum récupéré > 20 000 € => on récupère les valeurs telles quelles    |
  | Annuel de 13,00 Euros                                  | cas 12 (annuel salaire unique)  | null        | null        | salaire récupéré < 1666 € => on écrit NULL                                       |
  | Annuel de 1800,00 Euros                                | cas 12 (annuel salaire unique)  | 21600       | 21600       | salaire récupéré compris entre 1666 € et 20 000 € => on multiplie par 12         |
  | Annuel de 55000.0 Euros sur 12.0 mois                  | cas 12 (annuel salaire unique)  | 55000       | 55000       | salaire récupéré > 20 000 € => on récupère les valeurs telles quelles            |
  | Mensuel de 1000 Euros à 1300 Euros sur 12 mois         | cas 21 (mensuel fourchette)     | null        | null        | salaire minimum récupéré < 1666 € => on écrit NULL                               |
  | Mensuel de 1837.55 Euros à 2025.99 Euros sur 12.0 mois | cas 21 (mensuel fourchette)     | 22044       | 24300       | salaire minimum récupéré compris entre 1666 € et 20 000 € => on multiplie par 12 |
  | Mensuel de 30000.0 Euros à 35000.0 Euros sur 12.0 mois | cas 21 (mensuel fourchette)     | 30000       | 35000       | salaire minimum récupéré > 20 000 € => on récupère les valeurs telles quelles    |
  | Mensuel de 1000,00 Euros                               | cas 22 (mensuel salaire unique) | null        | null        | salaire récupéré < 1666 € => on écrit NULL                                       |
  | Mensuel de 3000,00 Euros                               | cas 22 (mensuel salaire unique) | 36000       | 36000       | salaire récupéré compris entre 1666 € et 20 000 € => on multiplie par 12         |
  | Mensuel de 45000.0 Euros sur 12.0 mois                 | cas 22 (mensuel salaire unique) | 45000       | 45000       | salaire récupéré > 20 000 € => on récupère les valeurs telles quelles            |
  | De 13,00 Euros à 14,00 Euros                           | cas 31 (mensuel ou annuel ?)    | null        | null        | salaire minimum récupéré < 1666 € => on écrit NULL                               |
  | Autre de 2000,00 Euros à 2195,00 Euros                 | cas 31 (mensuel ou annuel ?)    | 24000       | 26340       | salaire minimum récupéré compris entre 1666 € et 20 000 € => on multiplie par 12 |
  | Autre de 45000,00 Euros à 55000,00 Euros               | cas 31 (mensuel ou annuel ?)    | 45000       | 55000       | salaire minimum récupéré > 20 000 € => on récupère les valeurs telles quelles    |


### Analyse du jeu de données à travers des requêtes SQL

- voir le dossier "sql_requests/1_requests/offers_DE_DA_DS/"

- Au moins une requête sera faite pour chaque table de dimension pour mieux comprendre notre jeu de données.


## Power BI