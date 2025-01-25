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

    # table "Entreprises"
    nom_entreprise = offre.get("entreprise").get("nom")  # todo : certaines offres n'ont pas de nom d'entreprise (ex: 186JDCG)
    entreprise_adaptee = offre.get("entreprise").get("entrepriseAdaptee")

    # table "Secteurs"
    code_naf = offre.get("codeNAF")
    secteur_activite = offre.get("secteurActiviteLibelle")

    # table "Metiers"
    code_rome = offre.get("romeCode")
    appellation_rome = offre.get("appellationlibelle")

    # table "Experiences"
    libelle_experience = offre.get("experienceLibelle")
    code_exigence_experience = offre.get("experienceExige")
    commentaire_experience = offre.get("experienceCommentaire")

    # table "Contrats"
    code_type_contrat = offre.get("typeContrat")
    libelle_type_contrat = offre.get("typeContratLibelle")
    nature_contrat = offre.get("natureContrat")
    temps_travail = offre.get("complementExercice")
    condition_specifique = offre.get("conditionExercice")
    alternance = offre.get("alternance")

    # table "Qualifications"
    code_qualification = offre.get("qualificationCode")
    libelle_qualification = offre.get("qualificationLibelle")

    # table "Formations"
    libelle_formation = offre.get("formations", [{}])[0].get("niveauLibelle")
    code_exigence_formation = offre.get("formations", [{}])[0].get("exigence")

    # table "Competences"
    for item in offre.get("competences", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
        codes_competences = item.get("code")
        libelles_competences = item.get("libelle")
        codes_exigences_competences = item.get("exigence")
        # print(
        #     item,
        #     codes_competences,
        #     libelles_competences,
        #     codes_exigences_competences,
        #     sep="\n-> ",
        #     end="\n\n",
        # )

    print(id_offre)

    # table "QualitesProfessionnelles"
    for item in offre.get("qualitesProfessionnelles", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
        libelle_qualite_pro = item.get("libelle")
        description_qualite_pro = item.get("description")
        print(
            item,
            libelle_qualite_pro,
            description_qualite_pro,
            sep="\n-> ",
            end="\n\n",
        )
    break
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

    # table "OffreEmploi"
    # print(
    #     id_offre,
    #     intitule_offre,
    #     description_offre,
    #     date_creation,
    #     date_actualisation,
    #     nombre_postes,
    #     nom_partenaire,
    #     accessible_travailleurs_handicapes,
    #     difficile_a_pourvoir,
    #     sep="\n-> ",
    # )

    # table "Entreprises"
    # print(
    #     id_offre,
    #     nom_entreprise,
    #     entreprise_adaptee,
    #     sep="\n-> ",
    # )

    # table "Secteurs"
    # print(
    #     id_offre,
    #     code_naf,
    #     secteur_activite,
    #     sep="\n-> ",
    # )

    # table "Metiers"
    # print(
    #     id_offre,
    #     code_rome,
    #     appellation_rome,
    #     sep="\n-> ",
    # )

    # table "Experiences"
    # print(
    #     id_offre,
    #     libelle_experience,
    #     code_exigence_experience,
    #     commentaire_experience,
    #     sep="\n-> ",
    # )

    # table "Qualifications"
    # print(
    #     id_offre,
    #     code_qualification,
    #     libelle_qualification,
    #     sep="\n-> ",
    # )

    # table "Formations"
    # print(
    #     id_offre,
    #     libelle_formation,
    #     code_exigence_formation,
    #     sep="\n-> ",
    # )

    # table "Competences" (voir au-dessus car liste...)

    # table "QualitesProfessionnelles" (voir au-dessus car liste...)

    # table "Contrats"
    # print(
    #     id_offre,
    #     code_type_contrat,
    #     libelle_type_contrat,
    #     nature_contrat,
    #     temps_travail,
    #     condition_specifique,
    #     alternance,
    #     sep="\n-> ",
    # )


# conn.commit()  # Commit des changements

cursor.close()
conn.close()
