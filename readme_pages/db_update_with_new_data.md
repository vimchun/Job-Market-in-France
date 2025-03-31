- A la première exécution, on obtient une base de données avec notamment les attributs `offre_id` et `date_extraction = date_0` (date du jour où la première extraction a lieu).


- Tous les x jours, le process entier devra être ré-exécuté, et devra traiter les cas suivants, par exemple, à `date_1` qui correspond à une date postérieure à `date_0` :

  - Si une offre n'est plus disponible :

    - on ne supprime pas l'offre de la base
    - on laisse `date_extraction = date_0`
    - `to_process = False`


  - Si une offre est toujours disponible :

    - on ne supprime pas l'offre de la base
    - on met à jour `date_extraction = date_1`
    - on met à jour `date_actualisation` avec la nouvelle valeur
    - `to_process = False`


  - Si une offre est nouvelle :

    - on ajoute l'offre dans la base
    - on écrit `date_extraction = date_1`
    - `to_process = True`


- Le nouvel attribut `to_process` (booléen) servira à savoir si une offre doit repasser dans la "moulinette". En effet, une nouvelle offre devra subir les transformations suivantes :

  - Transformations côté Python :

    - Vérifier si la nouvelle offre est en France Métropolitaine (la conserver dans le cas positif, la rejeter sinon)

    - Ajout d'attributs nom/code des villes, communes, départements, régions à partir du code insee, coordonnées GPS, et autres informations


  - Transformations côté SQL :

    - Ajout d'un attribut pour savoir si une offre est pour un DA, un DE ou un DS

    - Ajout des attributs "salaire_min" et "salaire_max"