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

Dans le cas idéal, une offre est renseignée avec ses coordonnées GPS (latitude, longitude), le code postal et le code commune.

Toutefois, de nombreuses offres n'ont pas tous ces attributs renseignés, mais pour certaines d'entre-elles, il est possible de retrouver l'information.

En effet, l'attribut "libelle" peut parfois donner l'information, il peut prendre plusieurs formes :

  1. "69 - Lyon 3e Arrondissement" ou "69 - LYON 03"
    - (département - nom_commune)
    - A noter que le nom de la commune n'est pas toujours harmonisé ("Lyon 3e Arrondissement" vs "LYON 03"), ce qui complique la récupération du nom de la ville.

  1. "69" (juste le département)

  1. "Ile-de-France" (juste la région)

  1. "France" ou "FRANCE" ou "France entière"
    - Inutile dans notre cas, puisqu'on filtre déjà les offres en France Métropolitaine.

Dans les cas décrits par la suite, on part du cas le plus défavorable au cas le plus favorable :

Pour exemple, les cas suivants donneront une idée de pourcentage d'offres pour chacun des cas, à partir du notebook disponible en archive "_offres_concatenated_13639_offres__2025-03-05--22h09.json".

On part donc de 13 639 offres.

Pour "marquer" les offres, on va écrire pour chacune des offres si elle est dans le cas_01, dans le cas_02, etc... dans une colonne dédiée ("lieu_cas").

#### Cas 01 : quand libelle = ("FRANCE"|"France"|"France entière") (dans ce cas code postal = code commune = NAN), et latitude = longitude = NAN

Malheureusement, on ne peut tirer aucune information pour les offres qui sont dans ce cas.

Sur le json archivé, c'est le cas pour 252 offres sur 13 639, soit 1.85%.


#### Cas 02 : quand libelle = ("FRANCE"|"France"|"France entière") (dans ce cas code postal = code commune = NAN), et latitude/longitude sont renseignés


----------------------

quand code postal et/ou code commune sont renseignés

On peut retrouver la ville, le département et la région à partir du fichier csv.


#### Cas 2 : quand code postal et code commune ne sont pas renseignés, mais que les (bonnes) coordonnées GPS sont renseignées

On peut retrouver la ville


#### Cas 3 : quand code postal et code commune ne sont pas renseignés, mais que les (mauvaises) coordonnées GPS sont renseignées

Parfois, on peut avoir des coordonnées GPS renseignées, mais elles sont inversées.





