import json
import os
import sys

import psycopg2

# Booléens pour remplir ou pas les tables associées
fill_table_OffresEmploi = 1  # table "OffresEmploi"  ⛔ cette table doit être rempli pour pouvoir remplir les tables de liaison (dépendances)
fill_table_Entreprises = 0  # tables "Entreprises" + "Offre_Entreprise"
fill_table_Secteurs = 0  # table "Secteurs" + "Offre_Secteur"
fill_table_Metiers = 0  # table "Metiers" + "Offre_Metier"
fill_table_Experiences = 1  # table "Experiences" + "Offre_Experience"

current_directory = os.path.dirname(os.path.abspath(__file__))


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
        # "404278_Data_Engineer__5_offres.json",
        "_offres_merged.json",
    ),
    "r",
) as file:
    offres_data = json.load(file)
# print(offres_data)


def fill_db(db_name, attributes_tuple, on_conflict_string):
    """
    Crée et exécute la requête pour insérer les données dans la table spécifiée.
    Evite de devoir construire la requête et écrire <nombre_de_tables> fois :

        # cursor.execute(
        #     '''--sql
        #     INSERT INTO OffresEmploi (id_offre, intitule_offre, description_offre, date_creation, date_actualisation,
        #         nombre_postes, nom_partenaire, accessible_travailleurs_handicapes, difficile_a_pourvoir)
        #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        #     ON CONFLICT (id_offre)
        #         DO NOTHING
        #     ''',
        #     (id_offre, intitule_offre, description_offre, date_creation, date_actualisation,
        #     nombre_postes, nom_partenaire, accessible_travailleurs_handicapes, difficile_a_pourvoir)
        # )

    Ne retourne rien.
    """

    string_attributs = ", ".join(attributes_tuple)  # pour avoir "attribut1, attribut2, ..." sans les quotes
    placeholders = ", ".join(["%s"] * len(attributes_tuple))  # pour avoir "%s, %s, ..." pour chaque valeur

    dict_ = {attribut: globals().get(attribut) for attribut in attributes_tuple}

    # print(dict_)

    query = f"""
        INSERT INTO {db_name} ({string_attributs})
        VALUES ({placeholders})
        ON CONFLICT ({", ".join(on_conflict_string.split(" | "))}) DO NOTHING
    """

    # print(", ".join(on_conflict_string.split(" | ")))
    cursor.execute(query, tuple(dict_.values()))

    conn.commit()  # Commit des changements


def get_id_for_link_tables(id_name, table_name):
    """
    - Pour les tables de liaison entre une table 1 et une table 2, dans le cas où on a une table 2 avec un PK "serial",
       il faut récupérer l'identifiant de cette PK pour pouvoir faire un "INSERT INTO" dans la table de liaison.
       C'est le but de cette fonction.

    Retourne l'identifiant en question.
    """
    pass  # todo : à faire plus tard


conn = psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)

cursor = conn.cursor()


for offre in offres_data:
    # récupération de valeurs avec la méthode .get() au cas où il manquerait les clés dans certains documents jsons

    # table "OffresEmploi"
    id_offre = offre.get("id")
    intitule_offre = offre.get("intitule")
    description_offre = offre.get("description")
    date_creation = offre.get("dateCreation").split("T")[0]  # inutile de récupérer l'heure
    date_actualisation = offre.get("dateActualisation").split("T")[0]  # inutile de récupérer l'heure
    nombre_postes = offre.get("nombrePostes")
    nom_partenaire = offre.get("origineOffre").get("partenaires", [{}])[0].get("nom")
    accessible_travailleurs_handicapes = offre.get("accessibleTH")
    difficile_a_pourvoir = offre.get("offresManqueCandidats")

    if fill_table_OffresEmploi:
        fill_db(
            db_name="OffresEmploi",
            attributes_tuple=(
                "id_offre",
                "intitule_offre",
                "description_offre",
                "date_creation",
                "date_actualisation",
                "nombre_postes",
                "nom_partenaire",
                "accessible_travailleurs_handicapes",
                "difficile_a_pourvoir",
            ),
            on_conflict_string=("id_offre"),
        )

    # table "Entreprises"
    nom_entreprise = offre.get("entreprise").get("nom")
    if not nom_entreprise:  # certaines offres n'ont pas de nom d'entreprise (ex: 186JDCG)
        nom_entreprise = "NOM NON RENSEIGNÉ"
    entreprise_adaptee = offre.get("entreprise").get("entrepriseAdaptee")

    if fill_table_Entreprises:
        fill_db(
            db_name="Entreprises",
            attributes_tuple=(
                "nom_entreprise",
                "entreprise_adaptee",
            ),
            on_conflict_string="nom_entreprise",
        )

        fill_db(
            db_name="Offre_Entreprise",
            attributes_tuple=(
                "id_offre",
                "nom_entreprise",
            ),
            on_conflict_string="id_offre | nom_entreprise",
            # on_conflict_string="",
        )

    # table "Secteurs"
    code_naf = offre.get("codeNAF")
    secteur_activite = offre.get("secteurActiviteLibelle")

    if code_naf == None:  # gestion du cas où "codeNAF":null
        code_naf = "??????"  # rappel : attribut sur 6 chars

    if secteur_activite == None:  # gestion du cas où "secteurActivite":null
        secteur_activite = "Non spécifié"

    if fill_table_Secteurs:
        fill_db(
            db_name="Secteurs",
            attributes_tuple=(
                "code_naf",
                "secteur_activite",
            ),
            on_conflict_string="code_naf",
        )
        fill_db(
            db_name="Offre_Secteur",
            attributes_tuple=(
                "id_offre",
                "code_naf",
            ),
            on_conflict_string="id_offre | code_naf",
        )

    # table "Metiers"
    code_rome = offre.get("romeCode")
    appellation_rome = offre.get("appellationlibelle")

    if fill_table_Metiers:
        fill_db(
            db_name="Metiers",
            attributes_tuple=(
                "code_rome",
                "appellation_rome",
            ),
            on_conflict_string="code_rome",
        )
        fill_db(
            db_name="Offre_Metier",
            attributes_tuple=(
                "id_offre",
                "code_rome",
            ),
            on_conflict_string="id_offre | code_rome",
        )

    # table "Experiences"
    libelle_experience = offre.get("experienceLibelle")
    code_exigence_experience = offre.get("experienceExige")
    commentaire_experience = offre.get("experienceCommentaire")

    if fill_table_Experiences:
        fill_db(
            db_name="Experiences",
            attributes_tuple=(
                "libelle_experience",
                "code_exigence_experience",
                "commentaire_experience",
            ),
            on_conflict_string="libelle_experience | code_exigence_experience",
        )

        # Récupérer l'id pour pouvoir l'insérer en table
        query = f"""
            SELECT id_experience FROM Experiences
            WHERE libelle_experience = %s AND code_exigence_experience = %s
        """
        cursor.execute(query, (libelle_experience, code_exigence_experience))
        id_experience = cursor.fetchone()[0]

        fill_db(
            db_name="Offre_Experience",
            attributes_tuple=(
                "id_offre",
                "id_experience",
            ),
            on_conflict_string="id_offre | id_experience",
        )
    # break

    # table "Qualifications"
    code_qualification = offre.get("qualificationCode")
    libelle_qualification = offre.get("qualificationLibelle")

    # table "Formations"
    if offre.get("formations"):  # car on peut avoir dans le json "formations": null
        for item in offre.get("formations", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
            code_formation = offre.get("formations", [{}])[0].get("codeFormation")
            libelle_niveau_formation = offre.get("formations", [{}])[0].get("niveauLibelle")
            libelle_domaine_formation = offre.get("formations", [{}])[0].get("domaineLibelle")
            code_exigence_formation = offre.get("formations", [{}])[0].get("exigence")
            # print(item, code_formation, libelle_niveau_formation, libelle_domaine_formation, code_exigence_formation, sep="\n-> ", end="\n\n")

    # table "Competences"
    if offre.get("competences"):  # car on peut avoir dans le json "competences": null
        for item in offre.get("competences", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
            codes_competences = item.get("code")
            libelles_competences = item.get("libelle")
            codes_exigences_competences = item.get("exigence")
            # print(item, codes_competences, libelles_competences, codes_exigences_competences, sep="\n-> ", end="\n\n")

    # table "QualitesProfessionnelles"
    if offre.get("qualitesProfessionnelles"):  # car on peut avoir dans le json "qualitesProfessionnelles": null
        for item in offre.get("qualitesProfessionnelles", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
            libelle_qualite_pro = item.get("libelle")
            description_qualite_pro = item.get("description")
            # print(item, libelle_qualite_pro, description_qualite_pro, sep="\n-> ", end="\n\n")

    # table "Langues"
    if offre.get("langues"):  # car on peut avoir dans le json "langues": null
        for item in offre.get("langues", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
            libelle_langue = item.get("libelle")
            code_exigence_langue = item.get("exigence")
            # print(item, libelle_langue, code_exigence_langue, sep="\n-> ", end="\n\n")

    # table "PermisConduire"
    if offre.get("permis"):  # car on peut avoir dans le json "permis": null
        for item in offre.get("permis", []):
            libelle_permis = item.get("libelle")
            code_exigence_permis = item.get("exigence")
            # print(item, libelle_permis, code_exigence_permis, sep="\n-> ", end="\n\n")

    # table "LieuxTravail"
    code_commune = offre.get("lieuTravail").get("commune")
    latitude = offre.get("lieuTravail").get("latitude")
    longitude = offre.get("lieuTravail").get("longitude")

    # table "LieuxTravail_Ville"
    libelle_lieu_travail = offre.get("lieuTravail").get("libelle")
    code_postal = offre.get("lieuTravail").get("codePostal")

    # table "Contrats"
    code_type_contrat = offre.get("typeContrat")
    libelle_type_contrat = offre.get("typeContratLibelle")
    nature_contrat = offre.get("natureContrat")
    temps_travail = offre.get("complementExercice")
    condition_specifique = offre.get("conditionExercice")
    alternance = offre.get("alternance")

    # if id_offre == "185SYXS":
    #     break
    conn.commit()  # Commit des changements
    # break

    ### print() si besoin

    # table "OffresEmploi"
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
    ############## au-dessus : traité
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

    # table "Formations" (voir au-dessus car liste...)

    # table "Competences" (voir au-dessus car liste...)

    # table "QualitesProfessionnelles" (voir au-dessus car liste...)

    # table "Langues" (voir au-dessus car liste...)

    # table "PermisConduire" (voir au-dessus car liste...)

    # table "LieuxTravail"
    # print(
    #     id_offre,
    #     offre.get("lieuTravail"),
    #     code_commune,
    #     latitude,
    #     longitude,
    #     sep="\n-> ",
    # )

    # table "LieuxTravail_Ville"
    # print(
    #     id_offre,
    #     offre.get("lieuTravail"),
    #     libelle_lieu_travail,
    #     code_postal,
    #     sep="\n-> ",
    # )

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


cursor.close()
conn.close()
