"""
Ce fichier a des bouts de code non utilisés dans la chaîne finale end-to-end, mais ces bouts peuvent être utiles.
"""

import os

import pandas as pd

from functions import add_date_extract_attribute, add_date_premiere_ecriture_attribute

current_directory = os.path.dirname(os.path.abspath(__file__))
generated_json_files_directory = os.path.join(current_directory, "outputs", "offres", "1--generated_json_file")


json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]
json_filename = json_file_in_generated_directory[0]

if 0:
    """
    Prendre un json, et modifier ses attributs "dateExtraction" et "dateEcritureOffre"
    """

    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

    add_date_extract_attribute(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename,
        new_json_filename=json_filename,  # on écrase le fichier en entrée
        date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
    )

    add_date_premiere_ecriture_attribute(
        json_files_directory=generated_json_files_directory,
        json_filename=json_filename,
        new_json_filename=json_filename,  # on écrase le fichier en entrée
        date_to_insert="2025-03-02",  # à commenter si on veut mettre la date du jour
        overwrite_all_lines=False,
    )

    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

    print(
        # df.dateExtraction,
        df.dateEcritureOffre,
        sep="\n\n",
    )

if 0:
    """
    Réorganiser l'ordre des attributs.
    Dans l'exemple ci-dessous, l'attribut "dateExtraction" est placé en avant-dernière position (l'attribut était avant les attributs de localisation).
    """

    df = pd.read_json(os.path.join(generated_json_files_directory, json_filename), dtype=False)  # pour ne pas inférer les dtypes

    df = df[[ "id", "intitule", "description", "dateCreation", "dateActualisation", "romeCode", "romeLibelle", "appellationlibelle", "entreprise",
        "typeContrat", "typeContratLibelle", "natureContrat", "experienceExige", "experienceLibelle", "competences", "salaire", "dureeTravailLibelle",
        "dureeTravailLibelleConverti", "alternance", "contact", "agence", "nombrePostes", "accessibleTH", "deplacementCode", "deplacementLibelle",
        "qualificationCode", "qualificationLibelle", "codeNAF", "secteurActivite", "secteurActiviteLibelle", "qualitesProfessionnelles", "origineOffre",
        "offresManqueCandidats", "contexteTravail", "formations", "langues", "permis", "complementExercice", "experienceCommentaire", "conditionExercice",
        "lieu_cas", "code_insee", "nom_commune", "code_postal", "nom_ville", "code_departement", "nom_departement", "code_region", "nom_region",
        "dateExtraction", "datePremiereEcriture" ]]  # fmt: skip

    print(df)

    df.to_json(
        os.path.join(generated_json_files_directory, json_filename),
        orient="records",  # pour avoir une offre par document, sinon c'est toutes les offres dans un document
        force_ascii=False,  # pour convertir les caractères spéciaux
        indent=4,  # pour formatter la sortie
    )

    # On supprime les backslashs ajoutés par la méthode .to_json()
    with open(os.path.join(generated_json_files_directory, json_filename), "r", encoding="utf-8") as f:
        content = f.read()

        content = content.replace("\\/", "/")  # On remplace "\/" par "/"
        content = content.replace('":', '": ')  # On remplace les "deux-points sans espace" par des "deux-points avec espace"

        # On sauvegarde le fichier final sans les '\'
        with open(os.path.join(generated_json_files_directory, json_filename), "w", encoding="utf-8") as f:
            f.write(content)
