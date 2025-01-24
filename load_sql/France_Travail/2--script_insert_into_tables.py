import json
import os
import sys

import psycopg2

current_directory = os.path.dirname(os.path.abspath(__file__))

fill_offre = 1
fill_localisation = 1


with open(
    os.path.join(
        current_directory,
        "..",
        "..",
        "api_extract__transform",
        "France_Travail",
        "outputs",
        "_archives",
        "2025-01-13-exemples-jsons-et-json-merged",
        "404278_Data_Engineer__5_offres.json",
        # "_offres_merged.json",
    ),
    "r",
) as file:
    offres_data = json.load(file)
# print(offres_data)

conn = psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)

cursor = conn.cursor()


for offre in offres_data:
    # récupération de valeurs avec la méthode .get() au cas où il manquerait les clés dans certains documents jsons
    # table "OffreEmploi"
    id_offre = offre.get("id")
    intitule_offre = offre.get("intitule")
    description_offre = offre.get("description")
    date_creation = offre.get("dateCreation").split("T")[0]  # inutile de récupérer l'heure
    date_actualisation = offre.get("dateActualisation").split("T")[0]  # inutile de récupérer l'heure
    nombre_postes = offre.get("nombrePostes")
    nom_partenaire = offre.get("origineOffre").get("partenaires", [{}])[0].get("nom")
    accessible_travailleurs_handicapes = offre.get("accessibleTH")
    difficile_a_pourvoir = offre.get("offresManqueCandidats")

    print(
        # id_offre,
        # intitule_offre,
        # description_offre,
        # date_creation,
        # date_actualisation,
        # nombre_postes,
        # nom_partenaire,
        # accessible_travailleurs_handicapes,
        # difficile_a_pourvoir,
        sep="\n-> ",
    )

    # table "Contrats"
    description_offre_complement = offre.get("complementExercice", None)
    complementExercice = offre.get("complementExercice", "")
    accessibleTH = offre.get("accessibleTH", None)
    deplacementLibelle = offre.get("deplacementLibelle", None)
    qualificationLibelle = offre.get("qualificationLibelle", None)
    offresManqueCandidats = offre.get("offresManqueCandidats", None)
    complement_au_salaire_1 = offre.get("salaire", {}).get("complement1", None)  # ?? pas bon non ? prendre ligne suivante
    # break
    #
    # Insérer dans la table "offre"
    # cursor.execute(
    #     """--sql
    #     INSERT INTO offre (id, intitule, description, nombrePostes, accessibleTH, deplacementLibelle, qualificationLibelle, offresManqueCandidats, complementExercice)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     ON CONFLICT (id)
    #         DO NOTHING
    #     """,
    #     (
    #         id,
    #         intitule,
    #         description,
    #         nombrePostes,
    #         accessibleTH,
    #         deplacementLibelle,
    #         qualificationLibelle,
    #         offresManqueCandidats,
    #         complementExercice,
    #     ),
    # )

# conn.commit()  # Commit des changements

cursor.close()
conn.close()
