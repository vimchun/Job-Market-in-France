[Retour à la page principale](../README.md)

# Étape 1 : Extraction et transformation des données par API

- France Travail (https://francetravail.io/data/api) met à disposition plusieurs APIs, dont "Offres d'emploi v2" (`GET https://api.francetravail.io/partenaire/offresdemploi`).

- Le endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search` permet de récupérer les offres d'emploi actuelles selon plusieurs paramètres dont :

    - le code des appellations ROME pour filtrer par métier (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/appellations`) :

        ```json
        { "code": "38971",  "libelle": "Data analyst" },
        { "code": "38972",  "libelle": "Data scientist" },
        { "code": "404278", "libelle": "Data engineer" },
        ...
        ```

    - le code des pays (codes récupérés à partir du endpoint `GET https://api.francetravail.io/partenaire/offresdemploi/v2/referentiel/pays`) :

        ```json
        { "code": "01", "libelle": "France" },    // inclut les offres en France d'outre-mer et en Corse
        { "code": "02", "libelle": "Allemagne" }, // les pays étrangers ne retournent malheureusement pas d'offres sur les métiers à analyser
        ...
        ```

    - le paramètre `range` qui limite les résultats à 150 offres par requête (avec un status code à `206` si une requête renvoie plus de 150 offres), sachant que le nombre d'offres maximum récupérables est de 3150 offres.

        - Ainsi, si une requête peut renvoyer 351 offres, il faut enchainer 3 requêtes pour obtenir toutes les offres :
            - une première requête pour les offres `0-149` (status code 206),
            - une deuxième requête pour les offres `150-299` (status code 206),
            - une troisième requête pour les offres `300-350` (status code 200)

    - note : les paramètres liés aux dates (`minCreationDate`, `maxCreationDate`, `publieeDepuis`) ne permettent pas d'obtenir des offres expirées (celles qui ont permis de recruter quelqu'un).

- Cet API nous retourne des offres sous forme de documents json avec énormément d'attributs dont l'identifiant de l'offre, son intitulé, sa description, le lieu de travail, des informations sur l'entreprise et sur le contrat, les compétences demandées et l'expérience nécessaires, etc...

- Toutefois, l'API retourne aussi énormément d'offres sans lien avec le métier renseigné en paramètre (par exemple, une requête renseignant l'appellation "Data Engineer" peut renvoyer une offre telle que "Product Owner" car les termes "Data Engineer" peuvent être présents dans la description de l'offre d'emploi).

- Je requête ainsi un large panel de métiers, dont 29 ayant un lien avec la data, et 32 ayant un lien avec les métiers de la tech (dev, sécurité, devops...), pour maximiser les chances d'obtenir le plus d'offres d'emploi ayant un lien avec les métiers DE, DA et DS.

    - En effet, des offres de "Data Engineer" peuvent être présentes en requêtant l'appellation "Data_Manager" par exemple.

- Nous obtenons finalement 61 fichiers json contenant toutes les offres d'emploi liés ou pas à la data, pour la France et DOM-TOM uniquement car France Travail ne renvoie quasiment pas d'offre d'emploi pour les autres pays.

    - Ces 61 fichiers json seront concaténés dans un seul fichier json, où les doublons seront supprimés.

- A noter que les offres d"emploi retournées peuvent provenir soit de France Travail, soit des "partenaires", par exemple ("CADREMPLOI', "DIRECTEMPLOI", "INDEED", etc...)

<!--
todo : compléter avec :
0/ Supprimer les offres DOMTOM et Corse
1/ Extraire la ville, la commune, le département, et la région
2/ Ajouter un attribut pour savoir si l'offre est encore d'actualité ou pas
 -->

## Conservation des offres en France Métropolitaine uniquement

Pour une offre qui n'est pas en France Métropolitaine, l'attribut "libelle" donne l'information avec le "<département> - <nom_du_département>", par exemple :

- "971 - Guadeloupe"
- "974 - Réunion"
- "2A - Corse du Sud"
- "2B - BASTIA"

Les départements en France Métropolitaine ont 2 numéros, ceux en DOM-TOM ont 3 numéros, et ceux en Corse sont "2A" ou "2B".

Il est donc simple d'éliminer les offres en DOM-TOM et en Corse avec une regex "^(\d{3}|2(A|B))\s-\s", lorsque l'attribut "libelle" donne l'information avec le "<département> - <nom_du_département>".

On supprimera les offres lorsque l'attribut "libelle" donne l'information juste avec le nom du département si en dehors de la métropole, par exemple "Guadeloupe".


## Ajout d'attributs

### Ajout de la ville, du département et de la région

Les attributs "latitude", "longitude", "code_postal" et "code_commune" sont parfois renseignés.

Ils peuvent permettre de retrouver la ville, le département et/ou la région d'une offre d'emploi.

Dans les cas décrits par la suite, on part du cas le plus favorable au cas le plus défavorable :

Pour exemple, les cas suivants donneront une idée de pourcentage d'offres pour chacun des cas, à partir du notebook disponible en archive "_offres_concatenated_13639_offres__2025-03-05--22h09.json".

Ce json contient 13 639 offres.

Pour "marquer" les offres, on va écrire pour chacune des offres si elle est dans le cas_1, dans le cas_2, etc... dans une colonne dédiée ("lieu_cas").


#### Cas_1 : "code_commune" renseigné

Dans ce cas, on peut récupérer la ville, le département, et la région.

Sur le json archivé, c'est le cas pour 12 118 offres sur 13 639, soit 88.85% des offres.

todo : retrouver la ville, département, région

Notes :

- dans ce cas, il se peut que "code_postal" ne soit pas renseigné
- si code_commune = NAN, alors code_postal = NAN aussi (donc la colonne code_postal n'est pas utile pour retrouver la ville)


##### todo

On a donc le code commune.
A partir du fichier "ville_departement_region_names.csv", on va ajouter la ville, le département, et la région.


#### Cas_2 : "code_commune = NAN" (dans ce cas "code_postal = NAN"), mais coordonnées GPS renseignées

Sur le json archivé, c'est le cas pour 191 offres sur 13 639, soit 1.40% des offres.

Dans ce cas, on peut récupérer la ville, le département, et la région.

Ici, il y a 2 sous-cas : soit les coordonnées GPS sont corrects, soit la valeur de la latitude et la valeur de la longitude sont inversées.

On va se baser sur https://fr.wikipedia.org/wiki/Liste_de_points_extr%C3%AAmes_de_la_France pour trouver les variations des coordonnées GPS en France Métropolitaine.

En effet : - le point le plus au nord : (51° 05′ 21″ N, 2° 32′ 43″ E) - le point le plus au sud : (42° 19′ 58″ N, 2° 31′ 58″ E) - le point le plus à l'est : (48° 58′ 02″ N, 8° 13′ 50″ E) - le point le plus à l'ouest : (48° 24′ 46″ N, 4° 47′ 44″ O)

En convertissant ces coordonnées en valeur décimale, on trouve les fourchettes suivantes pour la latitude et la longitude de la France Métropolitaine :

    - Latitude : 42,3328 (Sud) -> 51,0892 (Nord)
    - Longitude : -4,7956 (Ouest) -> 8,2306 (Est)

Pour vérifier si la latitude a été inversée avec la longitude :
  - on vérifie si la latitude renseignée est bien comprise entre 42.3328 et 51.0892,
    - si oui, ça correspond à une latitude de la France Métropolitaine,
    - si non, on vérifie que la valeur renseignée pour la longitude l'est bien
      - si oui, on inversera la valeur de la latitude avec la valeur de la longitude.

todo : retrouver la ville, département, région


#### Cas_3 : "code_postal = code_commune = latitude = longitude = NAN", mais "libelle = 'numéro_département - nom_département'"

Sur le json archivé, c'est le cas pour 804 offres sur 13 639, soit 5.89% des offres.

Dans ce cas, on ne peut pas retrouver la ville, mais on peut retrouver le département, et par conséquent la région.

todo : retrouver le département, région



#### Cas_4 : "code_postal = code_commune = latitude = longitude = NAN", mais "libelle = nom_région"

Sur le json archivé, c'est le cas pour 54 offres sur 13 639, soit 0.39% des offres.

Ici, on a que la région, et on ne peut donc pas avoir la ville ni le département.


todo : écrire la région dans la colonne dédiée


#### Cas_5 : "code_postal = code_commune = latitude = longitude = NAN", et "libelle = ("FRANCE"|"France"|"France entière")"

Sur le json archivé, c'est le cas pour 252 offres sur 13 639, soit 1.85% des offres.

C'est le cas le plus défavorable qui ne permet pas de retrouver la ville, le département ni la région.

On pourrait aller plus loin, et tenter de retrouver l'information dans l'intitulé ou la description de l'offre d'emploi, mais on ne le fera pas ici.
