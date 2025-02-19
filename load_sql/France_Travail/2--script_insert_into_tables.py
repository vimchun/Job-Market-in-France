import json
import os

import psycopg2

# Booléens pour remplir ou pas les tables associées

fill_table_OffreEmploi = 0
fill_table_Contrat = 0
fill_table_Entreprise = 0
fill_table_Localisation = 0
fill_table_DescriptionOffre = 0
fill_table_Competence, fill_table_Offre_Competence = 0, 0
fill_table_Formation, fill_table_Offre_Formation = 0, 0
fill_table_Experience, fill_table_Offre_Experience = 0, 0
fill_table_QualiteProfessionnelle, fill_table_Offre_QualiteProfessionnelle = 0, 0
fill_table_Qualification, fill_table_Offre_Qualification = 0, 0
fill_table_Langue, fill_table_Offre_Langue = 0, 0
fill_table_PermisConduire, fill_table_Offre_PermisConduire = 0, 0

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


conn = psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432)

cursor = conn.cursor()


for offre in offres_data:
    # récupération de valeurs avec la méthode .get() au cas où il manquerait les clés dans certains documents jsons

    offre_id = offre.get("id")

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

    #### tables "Competence" + "Offre_Competence"

    if fill_table_Competence or fill_table_Offre_Competence:
        competences = offre.get("competences")  # ⛔ Attention on a une liste de compétences dans le json !!!

        if competences:
            for i in range(len(competences)):
                # /!\ note : il faut remplacer NULL par quelque chose (cas "competence_code = null")
                # /!\  (sinon risque d'écriture de doublon car "NULL != NULL selon la logique SQL")
                competence_code = competences[i].get("code", 0)
                competence_libelle = competences[i].get("libelle", "-")
                competence_code_exigence = competences[i].get("exigence", "-")

                # print(offre_id, competences, competence_code, competence_libelle, competence_code_exigence, sep="\n-> ", end="\n\n")

                #### table "Competence"

                if fill_table_Competence:
                    fill_db(
                        db_name="Competence",
                        attributes_tuple=(
                            "competence_code",
                            "competence_libelle",
                            "competence_code_exigence",
                        ),
                        on_conflict_string=("competence_code | competence_libelle | competence_code_exigence"),
                    )

                #### table "Offre_Competence"

                if fill_table_Offre_Competence:
                    # Récupérer l'id pour pouvoir l'insérer en table
                    query = f"""
                        SELECT competence_id FROM Competence
                        WHERE competence_code = %s AND competence_libelle = %s AND competence_code_exigence = %s
                    """
                    cursor.execute(query, (competence_code, competence_libelle, competence_code_exigence))
                    competence_id = cursor.fetchone()[0]

                    # print(offre_id, competence_code, competence_libelle, competence_code_exigence, competence_id, sep="\n-> ")

                    fill_db(
                        db_name="Offre_Competence",
                        attributes_tuple=(
                            "offre_id",
                            "competence_id",
                        ),
                        on_conflict_string="offre_id | competence_id",
                    )

    #### tables "Experience" + "Offre_Experience"

    if fill_table_Experience or fill_table_Offre_Experience:
        experience_libelle = offre.get("experienceLibelle")
        # if not experience_libelle:
        #     experience_libelle = "-"

        experience_code_exigence = offre.get("experienceExige")
        # if not experience_code_exigence:
        #     experience_code_exigence = "-"

        # parfois experience_commentaire existe bien et a la "null" dans le json
        experience_commentaire = offre.get("experienceCommentaire")
        if not experience_commentaire:
            experience_commentaire = "-"

        # print(offre_id, experience_libelle, experience_code_exigence, experience_commentaire, sep="\n-> ", end="\n\n")

        if experience_libelle != "-" or experience_code_exigence != "-" or experience_commentaire != "-":
            if fill_table_Experience:
                fill_db(
                    db_name="Experience",
                    attributes_tuple=(
                        "experience_libelle",
                        "experience_code_exigence",
                        "experience_commentaire",
                    ),
                    # on_conflict_string="experience_libelle | experience_code_exigence",
                    on_conflict_string="experience_libelle | experience_code_exigence | experience_commentaire",
                )

            if fill_table_Offre_Experience:
                # Requêter la table précédente pour récupérer l'id
                query = f"""
                    SELECT experience_id FROM Experience
                    WHERE experience_libelle = %s AND experience_code_exigence = %s AND experience_commentaire = %s
                """
                # cursor.execute(query, (experience_libelle, experience_code_exigence))
                cursor.execute(query, (experience_libelle, experience_code_exigence, experience_commentaire))
                experience_id = cursor.fetchone()[0]

                fill_db(
                    db_name="Offre_Experience",
                    attributes_tuple=(
                        "offre_id",
                        "experience_id",
                    ),
                    on_conflict_string="offre_id | experience_id",
                )

    #### tables "Formation" et "Offre_Formation"

    if fill_table_Formation or fill_table_Offre_Formation:
        formations = offre.get("formations", [{}])  # ⛔ Attention on a une liste de formations dans le json !!!

        if formations:
            for i in range(len(formations)):
                formation_code = formations[i].get("codeFormation", 0)
                formation_domaine_libelle = formations[i].get("domaineLibelle", "-")
                formation_niveau_libelle = formations[i].get("niveauLibelle", "-")
                formation_commentaire = formations[i].get("commentaire", "-")
                formation_code_exigence = formations[i].get("exigence", "-")

                # print(offre_id, formations[i], formation_code, formation_domaine_libelle, formation_niveau_libelle, formation_commentaire, formation_code_exigence, sep="\n-> ", end="\n\n")

                #### table "Formation"
                if fill_table_Formation:
                    fill_db(
                        db_name="Formation",
                        attributes_tuple=(
                            "formation_code",
                            "formation_domaine_libelle",
                            "formation_niveau_libelle",
                            "formation_commentaire",
                            "formation_code_exigence",
                        ),
                        on_conflict_string="formation_code | formation_domaine_libelle | formation_niveau_libelle | formation_commentaire | formation_code_exigence",
                    )

                #### table "Offre_Formation"
                if fill_table_Offre_Formation:
                    # Requêter la table précédente pour récupérer l'id
                    query = f"""
                        SELECT formation_id FROM Formation
                        WHERE formation_code = %s AND formation_domaine_libelle = %s AND formation_niveau_libelle = %s AND formation_commentaire = %s AND formation_code_exigence = %s
                    """

                    cursor.execute(query, (formation_code, formation_domaine_libelle, formation_niveau_libelle, formation_commentaire, formation_code_exigence))

                    formation_id = cursor.fetchone()[0]

                    # print(offre_id, formation_code, formation_domaine_libelle, formation_niveau_libelle, formation_commentaire, formation_code_exigence, formation_id, sep="\n-> ", end="\n\n")

                    fill_db(
                        db_name="Offre_Formation",
                        attributes_tuple=(
                            "offre_id",
                            "formation_id",
                        ),
                        on_conflict_string="offre_id | formation_id",
                    )

    #### tables "QualiteProfessionnelle" et "Offre_QualiteProfessionnelle"

    if fill_table_QualiteProfessionnelle or fill_table_Offre_QualiteProfessionnelle:
        qualites = offre.get("qualitesProfessionnelles")  # ⛔ Attention on a une liste de qualités professionnelles dans le json !!!

        if qualites:  # car on peut avoir dans le json "qualitesProfessionnelles": null
            for i in range(len(qualites)):
                qualite_professionnelle_libelle = qualites[i].get("libelle")
                qualite_professionnelle_description = qualites[i].get("description")

                # print(offre_id, qualites, qualite_professionnelle_libelle, qualite_professionnelle_description, sep="\n-> ", end="\n\n")

                #### table "QualiteProfessionnelle"
                if fill_table_QualiteProfessionnelle:
                    fill_db(
                        db_name="QualiteProfessionnelle",
                        attributes_tuple=(
                            "qualite_professionnelle_libelle",
                            "qualite_professionnelle_description",
                        ),
                        on_conflict_string=("qualite_professionnelle_libelle | qualite_professionnelle_description"),
                    )

                #### table "Offre_QualiteProfessionnelle"
                if fill_table_Offre_QualiteProfessionnelle:
                    # Récupérer l'id pour pouvoir l'insérer en table
                    query = f"""
                        SELECT qualite_professionnelle_id FROM QualiteProfessionnelle
                        WHERE qualite_professionnelle_libelle = %s AND qualite_professionnelle_description = %s
                    """
                    cursor.execute(query, (qualite_professionnelle_libelle, qualite_professionnelle_description))
                    qualite_professionnelle_id = cursor.fetchone()[0]

                    fill_db(
                        db_name="Offre_QualiteProfessionnelle",
                        attributes_tuple=(
                            "offre_id",
                            "qualite_professionnelle_id",
                        ),
                        on_conflict_string="offre_id | qualite_professionnelle_id",
                    )

    #### tables "Qualification" et "Offre_Qualification"
    if fill_table_Qualification or fill_table_Offre_Qualification:
        qualification_code = offre.get("qualificationCode")
        if not qualification_code:
            qualification_code = "-"

        qualification_libelle = offre.get("qualificationLibelle")
        if not qualification_libelle:
            qualification_libelle = "-"

        # print(offre_id, qualification_code, qualification_libelle, sep="\n-> ", end="\n\n")

        if qualification_code != "-" or qualification_libelle != "-":
            if fill_table_Qualification:
                fill_db(
                    db_name="Qualification",
                    attributes_tuple=(
                        "qualification_code",
                        "qualification_libelle",
                    ),
                    on_conflict_string="qualification_code | qualification_libelle",
                )

            if fill_table_Offre_Qualification:
                # Requêter la table précédente pour récupérer l'id
                query = f"""
                    SELECT qualification_code FROM Qualification
                    WHERE qualification_code = %s AND qualification_libelle = %s
                """
                cursor.execute(query, (qualification_code, qualification_libelle))
                qualification_code = cursor.fetchone()[0]

                fill_db(
                    db_name="Offre_Qualification",
                    attributes_tuple=(
                        "offre_id",
                        "qualification_code",
                    ),
                    on_conflict_string="offre_id | qualification_code",
                )

    # if offre_id == "186MCDP":
    # if offre_id == "186KTRN":
    #     break
    #### tables "Langue" et "Offre_Langue"
    if fill_table_Langue or fill_table_Offre_Langue:
        langues = offre.get("langues")  # ⛔ Attention on a une liste de langues dans le json !!!

        # print(offre_id, langues, sep="\n-> ", end="\n\n")

        if langues:
            for i in range(len(langues)):
                langue_libelle = langues[i].get("libelle")
                langue_code_exigence = langues[i].get("exigence")

                # print(offre_id, langues[i], langue_libelle, langue_code_exigence, sep="\n-> ", end="\n\n")

                #### table "Langue"
                if fill_table_Langue:
                    fill_db(
                        db_name="Langue",
                        attributes_tuple=(
                            "langue_libelle",
                            "langue_code_exigence",
                        ),
                        on_conflict_string=("langue_libelle | langue_code_exigence"),
                    )

                #### table "Offre_Langue"
                if fill_table_Offre_Langue:
                    # Récupérer l'id pour pouvoir l'insérer en table
                    query = f"""
                        SELECT langue_id FROM Langue
                        WHERE langue_libelle = %s AND langue_code_exigence = %s
                    """
                    cursor.execute(query, (langue_libelle, langue_code_exigence))
                    langue_id = cursor.fetchone()[0]

                    fill_db(
                        db_name="Offre_Langue",
                        attributes_tuple=(
                            "offre_id",
                            "langue_id",
                        ),
                        on_conflict_string="offre_id | langue_id",
                    )

    #### tables "PermisConduire" et "Offre_PermisConduire"

    if fill_table_PermisConduire or fill_table_Offre_PermisConduire:
        permisconduires = offre.get("permis")  # ⛔ Attention on a une liste de permisconduires dans le json !!!

        # print(offre_id, permisconduires, sep="\n-> ", end="\n\n")

        if permisconduires:
            for i in range(len(permisconduires)):
                permis_libelle = permisconduires[i].get("libelle")
                permis_code_exigence = permisconduires[i].get("exigence")

                # print(offre_id, permisconduires[i], permis_libelle, permis_code_exigence, sep="\n-> ", end="\n\n")

                #### table "PermisConduire"
                if fill_table_PermisConduire:
                    fill_db(
                        db_name="PermisConduire",
                        attributes_tuple=(
                            "permis_libelle",
                            "permis_code_exigence",
                        ),
                        on_conflict_string=("permis_libelle | permis_code_exigence"),
                    )

                #### table "Offre_PermisConduire"
                if fill_table_Offre_PermisConduire:
                    # Récupérer l'id pour pouvoir l'insérer en table
                    query = f"""
                        SELECT permis_id FROM permisconduire
                        WHERE permis_libelle = %s AND permis_code_exigence = %s
                    """
                    cursor.execute(query, (permis_libelle, permis_code_exigence))
                    permis_id = cursor.fetchone()[0]

                    fill_db(
                        db_name="Offre_PermisConduire",
                        attributes_tuple=(
                            "offre_id",
                            "permis_id",
                        ),
                        on_conflict_string="offre_id | permis_id",
                    )


cursor.close()
conn.close()
