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
        "api_extract_&_transform",
        "France_Travail",
        "outputs",
        "_archives",
        "2025-01-13-exemples-jsons-et-json-merged",
        # "404278_Data_Engineer__5_offres.json",
        "_offres_merged.json",
    ),
    "r",
) as file:
    offres_data = json.load(file)
# print(offres_data)
conn = psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)

cursor = conn.cursor()


if fill_offre:
    # Boucle pour insérer les données pour chaque offre
    for offre in offres_data:
        # utilisation de la méthode .get() au cas où il manquerait les clés dans certains documents jsons
        id = offre.get("id", None)
        intitule = offre.get("intitule", None)
        description = offre.get("description", None)
        nombrePostes = offre.get("nombrePostes", None)
        accessibleTH = offre.get("accessibleTH", None)
        deplacementLibelle = offre.get("deplacementLibelle", None)
        qualificationLibelle = offre.get("qualificationLibelle", None)
        offresManqueCandidats = offre.get("offresManqueCandidats", None)
        complementExercice = offre.get("salaire", {}).get("complement1", None)

        # Insérer dans la table "offre"
        cursor.execute(
            """--sql
            INSERT INTO offre (id, intitule, description, nombrePostes, accessibleTH, deplacementLibelle, qualificationLibelle, offresManqueCandidats, complementExercice)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
                DO NOTHING
            """,
            (
                id,
                intitule,
                description,
                nombrePostes,
                accessibleTH,
                deplacementLibelle,
                qualificationLibelle,
                offresManqueCandidats,
                complementExercice,
            ),
        )

    conn.commit()  # Commit des changements


if fill_localisation:
    for offre in offres_data:
        id = offre.get("id", None)
        lieu_travail = offre.get("lieuTravail", {})
        latitude = lieu_travail.get("latitude", None)
        longitude = lieu_travail.get("longitude", None)
        codePostal = lieu_travail.get("codePostal", None)

        cursor.execute(
            """--sql
            INSERT INTO localisation (id, latitude, longitude, codePostal)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """,
            (id, latitude, longitude, codePostal),
        )

    conn.commit()  # Commit des changements


cursor.close()
conn.close()
