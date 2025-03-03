[Retour à la page principale](../README.md)

# Étape 1 : Récolte des données par API

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