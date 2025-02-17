import json
import os
import sys

import psycopg2

# Booléens pour remplir ou pas les tables associées

#### OK
fill_table_OffreEmploi = 0
fill_table_Contrat = 0
fill_table_Entreprise = 0
fill_table_Localisation = 0
fill_table_DescriptionOffre = 0


#### en cours

#### todo
# fill_table_Entreprises = 0  # tables "Entreprises" + "Offre_Entreprise"
# fill_table_Secteurs = 0  # table "Secteurs" + "Offre_Secteur"
# fill_table_Metiers = 0  # table "Metiers" + "Offre_Metier"
# fill_table_Experiences = 1  # table "Experiences" + "Offre_Experience"

fill_table_Competence = 0
fill_table_Experience = 0
fill_table_NiveauFormation = 0
fill_table_DomaineFormation = 0
fill_table_QualiteProfessionnelle = 0
fill_table_Qualification = 0
fill_table_Langue = 0
fill_table_PermisConduire = 0
fill_table_Offre_Competence = 0
fill_table_Offre_Experience = 0
fill_table_Offre_NiveauFormation = 0
fill_table_Offre_DomaineFormation = 0
fill_table_Offre_QualiteProfessionnelle = 0
fill_table_Offre_Qualification = 0
fill_table_Offre_Langue = 0
fill_table_Offre_PermisConduire = 0


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
    Crée et exécute la requête pour insérer les données dans la table "db_name".
    Evite de devoir construire la requête et écrire <nombre_de_tables> fois :

        # cursor.execute(
        #     '''--sql
        #     INSERT INTO OffresEmploi (offre_id, intitule_offre, description_offre, date_creation, date_actualisation,
        #         nombre_postes, nom_partenaire, accessible_travailleurs_handicapes, difficile_a_pourvoir)
        #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        #     ON CONFLICT (offre_id)
        #         DO NOTHING
        #     ''',
        #     (offre_id, intitule_offre, description_offre, date_creation, date_actualisation,
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

    #### table "OffreEmploi"

    if fill_table_OffreEmploi:
        offre_id = offre.get("id")
        date_creation = offre.get("dateCreation").split("T")[0]  # inutile de récupérer l'heure
        date_actualisation = offre.get("dateActualisation").split("T")[0]  # inutile de récupérer l'heure
        nombre_postes = offre.get("nombrePostes")

        # print pour investigation si besoin
        print(
            offre_id,
            date_creation,
            date_actualisation,
            nombre_postes,
            sep="\n-> ",
        )

        fill_db(
            db_name="OffreEmploi",
            attributes_tuple=(
                "offre_id",
                "date_creation",
                "date_actualisation",
                "nombre_postes",
            ),
            on_conflict_string=("offre_id"),
        )

    #### table "Contrat"
    if fill_table_Contrat:
        offre_id = offre.get("id")
        type_contrat = offre.get("typeContrat")
        type_contrat_libelle = offre.get("typeContratLibelle")
        duree_travail_libelle = offre.get("dureeTravailLibelle")
        duree_travail_libelle_converti = offre.get("dureeTravailLibelleConverti")
        salaire_commentaire = offre.get("salaire").get("commentaire")
        salaire_libelle = offre.get("salaire").get("libelle")
        salaire_complement_1 = offre.get("salaire").get("complement1")
        salaire_complement_2 = offre.get("salaire").get("complement2")
        nature_contrat = offre.get("natureContrat")
        alternance = offre.get("alternance")
        deplacement_code = offre.get("deplacementCode")
        deplacement_libelle = offre.get("deplacementLibelle")
        temps_travail = offre.get("complementExercice")
        condition_specifique = offre.get("conditionExercice")

        # print pour investigation si besoin
        # print(
        #     offre_id,
        #     type_contrat,
        #     type_contrat_libelle,
        #     duree_travail_libelle,
        #     duree_travail_libelle_converti,
        #     salaire_commentaire,
        #     salaire_libelle,
        #     salaire_complement_1,
        #     salaire_complement_2,
        #     nature_contrat,
        #     alternance,
        #     deplacement_code,
        #     deplacement_libelle,
        #     temps_travail,
        #     condition_specifique,
        #     sep="\n-> ",
        # )
        # if offre_id == "185SYXS":
        #     break

        fill_db(
            db_name="Contrat",
            attributes_tuple=(
                "offre_id",
                "type_contrat",
                "type_contrat_libelle",
                "duree_travail_libelle",
                "duree_travail_libelle_converti",
                "salaire_commentaire",
                "salaire_libelle",
                "salaire_complement_1",
                "salaire_complement_2",
                "nature_contrat",
                "alternance",
                "deplacement_code",
                "deplacement_libelle",
                "temps_travail",
                "condition_specifique",
            ),
            on_conflict_string=("offre_id"),
        )

    #### table "Entreprise"
    if fill_table_Entreprise:
        offre_id = offre.get("id")
        nom_entreprise = offre.get("entreprise").get("nom")
        description_entreprise = offre.get("entreprise").get("description")
        # cas où nom_entreprise est la PK (ce n'est plus le cas) :
        #    if not nom_entreprise:  # certaines offres n'ont pas de nom d'entreprise (ex: 186JDCG)
        #        nom_entreprise = "NOM NON RENSEIGNÉ"
        code_naf = offre.get("codeNAF")
        secteur_activite_libelle = offre.get("secteurActiviteLibelle")
        entreprise_adaptee = offre.get("entreprise").get("entrepriseAdaptee")

        # print pour investigation si besoin
        # print(
        #     offre_id,
        #     nom_entreprise,
        #     description_entreprise,
        #     code_naf,
        #     secteur_activite_libelle,
        #     entreprise_adaptee,
        #     sep="\n-> ",
        # )

        fill_db(
            db_name="Entreprise",
            attributes_tuple=(
                "offre_id",
                "nom_entreprise",
                "description_entreprise",
                "code_naf",
                "secteur_activite_libelle",
                "entreprise_adaptee",
            ),
            on_conflict_string=("offre_id"),
        )

    #### table "Localisation"
    if fill_table_Localisation:
        offre_id = offre.get("id")
        description_lieu = offre.get("lieuTravail").get("libelle")
        code_commune = offre.get("lieuTravail").get("commune")
        code_postal = offre.get("lieuTravail").get("codePostal")
        # latitude = offre.get("lieuTravail").get("latitude")
        # longitude = offre.get("lieuTravail").get("longitude")

        # print pour investigation si besoin
        # print(
        #     offre_id,
        #     description_lieu,
        #     code_commune,
        #     code_postal,
        #     sep="\n-> ",
        # )

        fill_db(
            db_name="Localisation",
            attributes_tuple=(
                "offre_id",
                "description_lieu",
                "code_commune",
                "code_postal",
            ),
            on_conflict_string=("offre_id"),
        )

    #### table "DescriptionOffre"
    if fill_table_DescriptionOffre:
        offre_id = offre.get("id")
        description_offre = offre.get("description")
        nom_partenaire = offre.get("origineOffre").get("partenaires", [{}])[0].get("nom")
        rome_code = offre.get("romeCode")
        rome_libelle = offre.get("romeLibelle")
        appellation_rome = offre.get("appellationlibelle")
        difficile_a_pourvoir = offre.get("offresManqueCandidats")
        accessible_travailleurs_handicapes = offre.get("accessibleTH")

        # print pour investigation si besoin
        # print(
        #     offre_id,
        #     description_offre,
        #     nom_partenaire,
        #     rome_code,
        #     rome_libelle,
        #     appellation_rome,
        #     difficile_a_pourvoir,
        #     accessible_travailleurs_handicapes,
        #     sep="\n-> ",
        # )

        fill_db(
            db_name="DescriptionOffre",
            attributes_tuple=(
                "offre_id",
                "description_offre",
                "nom_partenaire",
                "rome_code",
                "rome_libelle",
                "appellation_rome",
                "difficile_a_pourvoir",
                "accessible_travailleurs_handicapes",
            ),
            on_conflict_string=("offre_id"),
        )

    ################### à nettoyer
    # table "Secteurs"
    # print(
    #     offre_id,
    #     code_naf,
    #     secteur_activite_libelle,
    #     sep="\n-> ",
    # )

    #    if fill_table_Entreprises:
    #        fill_db(
    #            db_name="Entreprises",
    #            attributes_tuple=(
    #                "nom_entreprise",
    #                "entreprise_adaptee",
    #            ),
    #            on_conflict_string="nom_entreprise",
    #        )

    #    # table "Secteurs"
    #    code_naf = offre.get("codeNAF")
    #    secteur_activite_libelle = offre.get("secteurActiviteLibelle")
    #
    #    if code_naf == None:  # gestion du cas où "codeNAF":null
    #        code_naf = "??????"  # rappel : attribut sur 6 chars
    #
    #    if secteur_activite_libelle == None:  # gestion du cas où "secteurActivite":null
    #        secteur_activite_libelle = "Non spécifié"
    #
    #    if fill_table_Secteurs:
    #        fill_db(
    #            db_name="Secteurs",
    #            attributes_tuple=(
    #                "code_naf",
    #                "secteur_activite_libelle",
    #            ),
    #            on_conflict_string="code_naf",
    #        )
    #        fill_db(
    #            db_name="Offre_Secteur",
    #            attributes_tuple=(
    #                "offre_id",
    #                "code_naf",
    #            ),
    #            on_conflict_string="offre_id | code_naf",
    #        )
    #

    #### pas bon mais pour archive
    #    fill_db(
    #        db_name="Offre_Entreprise",
    #        attributes_tuple=(
    #            "offre_id",
    #            "nom_entreprise",
    #        ),
    #        on_conflict_string="offre_id | nom_entreprise",
    #        # on_conflict_string="",
    #    )

    # conn.commit()  # Commit des changements
    # break

    #### reste des variables
    # intitule_offre = offre.get("intitule")

    #
    # "intitule_offre",
    # "description_offre",
    # "nom_partenaire",
    # "accessible_travailleurs_handicapes",
    # "difficile_a_pourvoir",
    ####

    #
    #    # table "Metiers"
    #
    #    if fill_table_Metiers:
    #        fill_db(
    #            db_name="Metiers",
    #            attributes_tuple=(
    #                "rome_code",
    #                "appellation_rome",
    #            ),
    #            on_conflict_string="rome_code",
    #        )
    #        fill_db(
    #            db_name="Offre_Metier",
    #            attributes_tuple=(
    #                "offre_id",
    #                "rome_code",
    #            ),
    #            on_conflict_string="offre_id | rome_code",
    #        )
    #
    #    # table "Experiences"
    #    experience_libelle = offre.get("experienceLibelle")
    #    experience_code_exigence = offre.get("experienceExige")
    #    experience_commentaire = offre.get("experienceCommentaire")
    #
    #    if fill_table_Experiences:
    #        fill_db(
    #            db_name="Experiences",
    #            attributes_tuple=(
    #                "experience_libelle",
    #                "experience_code_exigence",
    #                "experience_commentaire",
    #            ),
    #            on_conflict_string="experience_libelle | experience_code_exigence",
    #        )
    #
    #        # Récupérer l'id pour pouvoir l'insérer en table
    #        query = f"""
    #            SELECT id_experience FROM Experiences
    #            WHERE experience_libelle = %s AND experience_code_exigence = %s
    #        """
    #        cursor.execute(query, (experience_libelle, experience_code_exigence))
    #        id_experience = cursor.fetchone()[0]
    #
    #        fill_db(
    #            db_name="Offre_Experience",
    #            attributes_tuple=(
    #                "offre_id",
    #                "id_experience",
    #            ),
    #            on_conflict_string="offre_id | id_experience",
    #        )
    #    # break
    #
    #    # table "Qualifications"
    #    qualification_code = offre.get("qualificationCode")
    #    qualification_libelle = offre.get("qualificationLibelle")
    #
    #    # table "Formations"
    #    if offre.get("formations"):  # car on peut avoir dans le json "formations": null
    #        for item in offre.get("formations", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
    #            formation_code = offre.get("formations", [{}])[0].get("codeFormation")
    #            niveau_formation_libelle = offre.get("formations", [{}])[0].get("niveauLibelle")
    #            formation_domaine_libelle = offre.get("formations", [{}])[0].get("domaineLibelle")
    #            formation_code_exigence = offre.get("formations", [{}])[0].get("exigence")
    #            # print(item, formation_code, niveau_formation_libelle, formation_domaine_libelle, formation_code_exigence, sep="\n-> ", end="\n\n")
    #
    #    # table "Competences"
    #    if offre.get("competences"):  # car on peut avoir dans le json "competences": null
    #        for item in offre.get("competences", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
    #            codes_competences = item.get("code")
    #            libelles_competences = item.get("libelle")
    #            codes_exigences_competences = item.get("exigence")
    #            # print(item, codes_competences, libelles_competences, codes_exigences_competences, sep="\n-> ", end="\n\n")
    #
    #    # table "QualitesProfessionnelles"
    #    if offre.get("qualitesProfessionnelles"):  # car on peut avoir dans le json "qualitesProfessionnelles": null
    #        for item in offre.get("qualitesProfessionnelles", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
    #            qualite_professionnelle_libelle = item.get("libelle")
    #            qualite_professionnelle_description = item.get("description")
    #            # print(item, qualite_professionnelle_libelle, qualite_professionnelle_description, sep="\n-> ", end="\n\n")
    #
    #    # table "Langues"
    #    if offre.get("langues"):  # car on peut avoir dans le json "langues": null
    #        for item in offre.get("langues", []):  # liste de dictionnaires ("[]" si la clé n'existe pas pour une offre)
    #            langue_libelle = item.get("libelle")
    #            langue_code_exigence = item.get("exigence")
    #            # print(item, langue_libelle, langue_code_exigence, sep="\n-> ", end="\n\n")
    #
    #    # table "PermisConduire"
    #    if offre.get("permis"):  # car on peut avoir dans le json "permis": null
    #        for item in offre.get("permis", []):
    #            permis_libelle = item.get("libelle")
    #            permis_code_exigence = item.get("exigence")
    #            # print(item, permis_libelle, permis_code_exigence, sep="\n-> ", end="\n\n")
    #
    #
    #

    # intitule_offre,
    # description_offre,
    # nom_partenaire,
    # accessible_travailleurs_handicapes,
    # difficile_a_pourvoir,

    # table "Metiers"
    # print(
    #     offre_id,
    #     rome_code,
    #     appellation_rome,
    #     sep="\n-> ",
    # )

    # table "Experiences"
    # print(
    #     offre_id,
    #     experience_libelle,
    #     experience_code_exigence,
    #     experience_commentaire,
    #     sep="\n-> ",
    # )

    # table "Qualifications"
    # print(
    #     offre_id,
    #     qualification_code,
    #     qualification_libelle,
    #     sep="\n-> ",
    # )

    # table "Formations" (voir au-dessus car liste...)

    # table "Competences" (voir au-dessus car liste...)

    # table "QualitesProfessionnelles" (voir au-dessus car liste...)

    # table "Langues" (voir au-dessus car liste...)

    # table "PermisConduire" (voir au-dessus car liste...)

    # table "LieuxTravail"
    # print(
    #     offre_id,
    #     offre.get("lieuTravail"),
    #     code_commune,
    #     latitude,
    #     longitude,
    #     sep="\n-> ",
    # )

    # table "LieuxTravail_Ville"
    # print(
    #     offre_id,
    #     offre.get("lieuTravail"),
    #     libelle_lieu_travail,
    #     code_postal,
    #     sep="\n-> ",
    # )


cursor.close()
conn.close()
