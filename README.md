# Table des matières

- [Étape 1 : Récolte des données par API](#étape-1--récolte-des-données-par-API)

ajouter la partie "adzuna"
ajouter la partie "the muse"

# Projet Job Market


(repris de la fiche)

- Ce projet a pour but de mettre en avant nos compétences de Data Engineer.

- Nous allons regrouper des informations sur les offres d’emplois et les compagnies qui les proposent.

- À la fin du projet, nous aurons une meilleure vision du marché de l’emploi :
  - quels secteurs recrutent le plus
  - quelles compétences sont requises
  - quelles sont les villes les plus actives
  - etc …
  - idées à creuser :
    - quelles sont les régions les plus actives
    - top30 des entreprises qui recrutent le plus
    - carte de France de densité de recrutement
    - comparatifs métiers DE/DS/DA



## Étape 1 : Récolte des données par API

### API de "France Travail"

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
  - les offres n'ont parfois pas de lien avec le libellé renseigné en paramètre
    - Par exemple, une requête renseignant l'appellation "404278" (pour "Data Engineer") peut renvoyer une offre telle que "Product Owner".
  - une offre de "Data Engineer" peut se retrouver dans des résultats dont les requêtes utilisent une appellation autre que "404278"
    - Par exemple, nous avons vu des offres de "Data Engineer" en requêtant avec l'appellation "38975" (pour "Data_Manager").
  - nous voulons filtrer sur un métier spécifique
    - Par exemple, pour filtrer sur le métier de "Data Engineer", nous pouvons filtrer sur la chaîne de caractères "Ingénieur Data" et vérifier si celle-ci est présente dans l'intitulé, mais il faut exclure les offres retournées telles que "Ingénieur Data Scientist". Nous rajoutons d'autres chaînes de caractères telles que "Data Engineer", et d'autres possibilités en cas de typo du recruteur qu'il faut gérer (par exemple, nous avons vu une offre "Data Ingineer").

- Nous obtenons finalement un fichier json contenant toutes les offres d'emploi pour le métier que nous souhaitons.



### API de "The Muse"

L'API `GET https://www.themuse.com/api/public/jobs` permet de récupérer les offres d'emploi sur 3 critères principales :
  - la catégorie du métier ("category")
    - par exemple : "Data and Analytics", "Data Science"
  - le niveau d'expérience requis pour l'offre ("level")
    - par exemple : "Entry Level", "Mid Level", "Senior Level"
  - la localisation ("location")
    - par exemple "Paris, France"
    - il y a près de 21 000 villes proposés, dont 409 villes françaises, que nous devons sélectionner pour la requête (ce qui fait une requête énorme)

Parmi les résultats, les offres de télétravail sont présentes (on veut les retirer ? sûrement oui).

Une requête donne au maximum 20 offres, nous faisons donc une requête initiale pour voir combien de requêtes sont nécessaires pour récupérer toutes les offres (clé "page_count" de la réponse).