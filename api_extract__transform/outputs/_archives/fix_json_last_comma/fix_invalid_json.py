import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
invalid_json = os.path.join(current_directory, "invalid_json.json")
valid_json = os.path.join(current_directory, "valid_json.json")


"""
Le code suivant est utilisé dans la fonction .get_offres(), pour rendre un json invalide (généré par cette fonction) valide.

En effet, les json créés pour chaque appellation sont de cette forme (simplifiée en ne conservant ici que 3 offres, et 2 attributs) :

    ```
    [
    {"id": "188VMGQ", "intitule": "Data Engineer (H/F)"},
    {"id": "188RQRZ", "intitule": "Responsable Data Studio F/H (H/F)"},
    {"id": "188PNVQ", "intitule": "Maître du Jeu des ETL recherché pour notre Next Game"},
        // ligne vide
    ```

Ces json sont évidemment invalides, et ce script a pour but de rendre ces json valides.

L'exemple précédent donnerait en appliquant le script :

    ```
    [
    {"id": "188VMGQ", "intitule": "Data Engineer (H/F)"},
    {"id": "188RQRZ", "intitule": "Responsable Data Studio F/H (H/F)"},
    {"id": "188PNVQ", "intitule": "Maître du Jeu des ETL recherché pour notre Next Game"}  // sans le trailing comma
    ]                                                                                      // avec le crochet fermant
    ```

Ce script écrit le json valide dans un autre fichier, mais dans le fichier "functions.py", cela sera fait directement dans le même fichier json.

"""


# Ecrire le contenu de "invalid_json.json" dans "invalid_content"
with open(invalid_json, "r") as invalid:
    invalid_content = invalid.read()

# Ecrire le json valide dans "valid_content"
with open(valid_json, "w") as valid:
    valid_content = invalid_content[:-2] + "\n]"
    valid.write(valid_content)

# Ouvrir le fichier json valide pour vérifier qu'il est bien valide
with open(valid_json, "r") as valid:
    valid_content = valid.read()
    # print(valid_content)
    try:
        json.loads(valid_content)
        print("Le json est bien valide.")
        # print(parsed_json)
    except json.JSONDecodeError as e:
        print(f"Le json n'est pas valide :\n==> {e}")
