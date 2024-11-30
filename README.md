# Table des matières

- [Étape 1 : Récolte des données](#étape-1--récolte-des-données)


# Projet Job Market


(repris de la fiche)

- Ce projet a pour but de mettre en avant nos compétences de Data Engineer.

- Nous allons regrouper des informations sur les offres d’emplois et les compagnies qui les proposent.

- À la fin du projet, nous aurons une meilleure vision du marché de l’emploi :
  - quels secteurs recrutent le plus
  - quelles compétences sont requises
  - quelles sont les villes les plus actives
  - etc …



## Étape 1 : Récolte des données

- France Travail (https://francetravail.io/data/api) met à disposition 18 APIs pour récolter diverses données.
- Nous utilisons l'API "Offres d'emploi" pour rechercher des offres selon plusieurs paramètres.
  - Ainsi, pour un métier donné, nous aurons des informations sur les secteurs qui recrutent le plus grâce au code NAF, les compétences requises, les villes qui recrutent le plus...

- Parmi les paramètres que nous utilisons le plus, il y a :

  - le paramètre `range` :
    - qui limite les résultats à 150 offres par requête (status code 206 si un filtre peut renvoyer plus de 150 offres).
    - qui limite le nombre total d'offres récupérables à 3150 offres.

    - par exemple, si un filtre peut renvoyer 351 offres, il faut enchainer les requêtes pour obtenir toutes les offres :
      - requête 1 pour les offres `0-149` (status code 206), puis requête 2 pour les offres `150-299` (status code 206), puis requête 3 pour les offres `300-350` (status code 200)

  - le paramètre `appellation`, pour récupérer les offres de tous les métiers ayant un lien avec la data :

    ```json
    # métiers en lien avec Data Engineer
    { "code": "404278", "libelle": "Data engineer" },
    { "code": "404282", "libelle": "Ingénieur / Ingénieure big data" },
    {...}
    # autres métiers de la Data
    { "code": "38971", "libelle": "Data analyst" },
    { "code": "38972", "libelle": "Data scientist" },
    {...}
    ```
  - <compléter avec les paramètres qui permettront de récupérer plus d'offres>

- Cet API nous retourne des offres sous forme de documents json avec beaucoup d'informations dont l'identifiant de l'offre, son intitulé, sa description, le lieu de travail, des informations sur l'entreprise et sur le contrat, les compétences demandées et l'expérience nécessaires, etc...

- Nous filtrons ensuite à nouveau sur les offres retournées en vérifiant si telles chaînes de charactère sont présentes dans l'intitulé d'une offre, pour les raisons suivantes :
  - elles n'ont parfois pas de lien avec le libellé renseigné en paramètre, par exemple une requête renseignant l'appellation "404278" (pour "Data Engineer") peut renvoyer une offre telle que "Product Owner".
  - nous voulons filtrer sur un métier spécifique (par exemple le métier de "Data Engineer")
  - une offre de "Data Engineer" peut se retrouver dans des résultats dont les requêtes utilisent une appellation autre que "404278", par exemple nous avons vu des offres de "Data Engineer" en requêtant avec l'appellation "38975" (pour "Data_Manager")

- Nous obtenons finalement un fichier json contenant toutes les offres d'emploi pour le métier que nous souhaitons.