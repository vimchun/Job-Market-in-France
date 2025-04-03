# Ce qu'on avait avant les travaux et ce qu'il faut modifier


## Ce qu'on avait avant les travaux

La moulinette Python crée les fichiers suivants dans le dossier "api_extract__transform/outputs/offres" :

  - `concatenate_all_json_into_one()` :
        => json_generated_filename_0 = "2025-03-05--22h09__0__all__13639_offres.json"

  - `add_date_extract_attribute()` :
        => json_generated_filename_1 = "2025-03-05--22h09__1__all__13639_offres__with_date_extraction_attribute.json"

  - `keep_only_offres_from_metropole()` :
        => json_generated_filename_2 = "2025-03-05--22h09__2__only_metropole__13419_offres.json"

  - `add_location_attributes()` :
        => json_generated_filename_3 = "2025-03-05--22h09__3__with_location_attributes.json"


## Ce qu'il faut modifier

- Il n'est pas nécessaire d'avoir les fichiers json intermédiaires, donc chaque méthode écrasera le fichier qu'il a en entrée.

- Optimisation du temps d'exécution :

  - Les fonctions `add_date_extract_attribute()` et `keep_only_offres_from_metropole()` ne prennent que quelques secondes d'exécution.
  - Par contre, `add_location_attributes()` prend 3-5 minutes.
    - Pour éviter de refaire le travail de recherche de localisation pour chaque offre d'emploi, on créera l'attribut `offre_localise` (offre localisé), un booléen qui vaudra `False` si `add_location_attributes()` n'a pas traité l'offre d'emploi.

- Comment savoir si le script a déjà été exécuté ?

  - Si un fichier json n'existe pas dans `api_extract__transform/outputs/offres/1--generated_json_file` :

    - cela signifie que le script n'a jamais été exécuté


  - Si un fichier json existe déjà dans `api_extract__transform/outputs/offres/1--generated_json_file` :

    - cela signifie que le script a déjà été exécuté

    - on connait le nombre d'occurence :
      - si le fichier s'appelle "2025-04-02--14h40__extraction__occurence_1.json", cela signifie qu'il n'y a eu qu'une seule occurence
      - si le fichier s'appelle "2025-04-04--21h14__extraction__occurence_5.json", cela signifie qu'il y a eu 5 occurences
    - le script `extract_and_transform_data.py` doit lorsqu'il est lancé :
      - vérifier l'absence ou la présence d'un fichier json dans `api_extract__transform/outputs/offres/1--generated_json_file` (ce dossier ne contient soit pas de json, soit qu'un seul (pas plusieurs, comme le mentionne le fichier dans ce dossier qui se nomme `_this_folder_should_contain_0_or_1_json_file_`)) :

        - s'il y a un fichier json, le script `extract_and_transform_data.py` devrait mettre à jour la date et l'heure avec le moment où il est lancé, par exemple  "2025-04-02--20h40__extraction__occurence_2.json", le point important est d'avoir "__extraction__occurence_2.json" qui montre que le numéro dans le nom du fichier a été incrémenter

        - s'il n'y a pas de fichier json, le script `extract_and_transform_data.py` devrait créer un fichier json, par exemple  "2025-04-02--14h40__extraction__occurence_1.json", le point important est d'avoir "__extraction__occurence_1.json" qui mentionne qu'il s'agit de la première occurence

        - s'il contient plusieurs fichiers json, on arrête le script.



# todo : Mise à jour de la base avec les nouvelles données

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