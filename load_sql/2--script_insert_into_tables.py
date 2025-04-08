import json
import os

import psycopg2

"""
Notes :
  - Pour remplir les 19 tables, pour ~14k offres et ~60 attributs :
    - met environ 11 minutes si .commit() dans la base pour chaque ligne
    - met environ 3 minutes si .commit() dans la base en fin de script
"""


# Booléens pour remplir ou pas les tables associées
fill_table_OffreEmploi = 1
fill_table_Contrat = 1
fill_table_Entreprise = 1
fill_table_Localisation = 1
fill_table_DescriptionOffre = 1
fill_table_Competence, fill_table_Offre_Competence = 1, 1
fill_table_Experience, fill_table_Offre_Experience = 1, 1
fill_table_Formation, fill_table_Offre_Formation = 1, 1
fill_table_QualiteProfessionnelle, fill_table_Offre_QualiteProfessionnelle = 1, 1
fill_table_Qualification, fill_table_Offre_Qualification = 1, 1
fill_table_Langue, fill_table_Offre_Langue = 1, 1
fill_table_PermisConduire, fill_table_Offre_PermisConduire = 1, 1

current_directory = os.path.dirname(os.path.abspath(__file__))

sql_safe_null = "Ceci est un string qui figure nulle part dans le json pour pouvoir écrire les NULL sans doublon"  # ne peut pas être "-" car cette valeur peut exister

# Charger le fichier json dans le dossier "1--generated_json_file"
generated_json_files_directory = os.path.join(current_directory, "..", "api_extract__transform", "outputs", "offres", "1--generated_json_file")
json_file_in_generated_directory = [file for file in os.listdir(generated_json_files_directory) if file.endswith(".json")]

assert len(json_file_in_generated_directory) == 1  # On doit avoir un seul fichier json dans le dossier

current_json_file = json_file_in_generated_directory[0]  # exemple : 2025-04-02--15h52__extraction_occurence_1.json


with open(
    os.path.join(
        generated_json_files_directory,
        #
        # current_json_file,
        #
        # "archive_json_files", "2025-03-02--18h36__extraction_occurence_1.json",
        "archive_json_files", "2025-04-05--21h48__extraction_occurence_2.json",
        #
        # "troubleshooting", "test_with_few_documents_occurence_1.json",
        # "troubleshooting", "test_with_few_documents_occurence_2.json",
    ),
    "r",
) as file:  # fmt: off
    offres_data = json.load(file)


def fill_db(db_name, attributes_tuple, on_conflict_string):
    """
    Crée et exécute la requête pour insérer les données dans la table "db_name".

    Évite de devoir construire la requête, et de devoir dupliquer certaines informations comme les attributs.


    Exemple dans le code suivant où on écrit l'attribut date_extraction 4 fois :

        cursor.execute(
            f'''--sql
                INSERT INTO OffreEmploi (offre_id, date_extraction, date_creation, date_actualisation, nombre_postes)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (offre_id) DO UPDATE SET
                    date_extraction = EXCLUDED.date_extraction,
                    date_creation = EXCLUDED.date_creation,
                    date_actualisation = EXCLUDED.date_actualisation,
                    nombre_postes = EXCLUDED.nombre_postes
                ''',
            (offre_id, date_extraction, date_creation, date_actualisation, nombre_postes),
        )

    Avec la fonction, on ne l'écrit plus qu'1 fois :

        fill_db(
            db_name="OffreEmploi",
            attributes_tuple=(
                "offre_id",
                "date_extraction",
                "date_creation",
                "date_actualisation",
                "nombre_postes",
            ),
            on_conflict_string=("offre_id"),
        )

    https://www.postgresql.org/docs/current/sql-insert.html

    Ne retourne rien.
    """

    string_attributs = ", ".join(attributes_tuple)  # pour avoir "attribut1, attribut2, ..." sans les quotes
    placeholders = ", ".join(["%s"] * len(attributes_tuple))  # pour avoir "%s, %s, ..." pour chaque valeur

    # dict_ = {attribut: globals().get(attribut) for attribut in attributes_tuple}

    query = f"""
        INSERT INTO {db_name} ({string_attributs})
        VALUES ({placeholders})
        ON CONFLICT ({", ".join(on_conflict_string.split(" | "))})
    """

    # Déterminer les colonnes à mettre à jour (toutes sauf celles de la clé)
    update_cols = [f"{attr} = EXCLUDED.{attr}" for attr in attributes_tuple if attr not in on_conflict_string.split(" | ")]

    if update_cols:
        query += f"""DO UPDATE SET {", ".join(update_cols)}"""
    else:
        query += "DO NOTHING"

    cursor.execute(query, tuple(globals().get(attr) for attr in attributes_tuple))
    # conn.commit()  # pas besoin car fait implicitement par la suite avec "with conn.cursor()"

    return None


with psycopg2.connect(database="francetravail", host="localhost", user="mhh", password="mhh", port=5432) as conn:
    with conn.cursor() as cursor:  # pas besoin de faire conn.commit()
        ##################
        #### PARTIE 1 ####
        ##################

        """
        Dans cette boucle for, pour toutes les tables de dimension qui ont une table de liaison, on traite les tables de dimension en remplaçant les null par une valeur quelconque.
            (sinon on risque d'écrire des doublons, car NULL != NULL en SQL)

            Par exemple, pour la table Formation, si on récupère pour une offre les valeurs suivantes :

               "formation_code"            = 31026
               "formation_domaine_libelle" = "data science"
               "formation_niveau_libelle"  = "Bac+5 et plus ou équivalents"
               "formation_commentaire"     = null
               "formation_code_exigence"   = "S"

               => alors on va écrire les données correspondantes en base, n'ayant pas de contrainte NOT NULL sur "formation commentaire".
                  (en effet, on a "formation_commentaire = null", cela serait dommage de rejeter l'information)

                    CREATE TABLE Formation (
                        formation_id SERIAL NOT NULL PRIMARY KEY
                        , formation_code INTEGER
                        , formation_domaine_libelle VARCHAR(100)
                        , formation_niveau_libelle VARCHAR(30)
                        , formation_commentaire VARCHAR(100)    -- pas de contrainte NOT NULL
                        , formation_code_exigence VARCHAR(1)
                        , CONSTRAINT formation_unique UNIQUE (formation_code , formation_domaine_libelle , formation_niveau_libelle , formation_commentaire , formation_code_exigence)
                    );


            Mais si une autre offre a exactement ces mêmes valeurs (avec "formation_commentaire = null"), on pourrait s'attendre à ce qu'on n'écrive pas cette ligne grâce à la contrainte d'unicité.
            Or, cette nouvelle ligne sera quand même écrite, cela étant sûrement lié au fait que "null != null" sur SQL.

            Donc pour contourner cela, pour toutes les offres, on va remplacer null par une valeur, par exemple :

               "formation_code"            = 31026
               "formation_domaine_libelle" = "data science"
               "formation_niveau_libelle"  = "Bac+5 et plus ou équivalents"
               "formation_commentaire"     = value_not_existing_in_json  # précédemment null
               "formation_code_exigence"   = "S"

               => ainsi, si une autre offre a de nouveau exactement ces mêmes valeurs, alors cette nouvelle offre ne sera pas écrite en base, grâce à la contrainte d'unicité.


        La seconde étape de ce script réécrit ces valeurs à null.

        """

        # récupération de valeurs avec la méthode .get() au cas où il manquerait les clés dans certains documents jsons

        #### table "OffreEmploi"

        if fill_table_OffreEmploi:
            print("Écriture de la table OffreEmploi")

            for offre in offres_data:
                offre_id = offre.get("id")
                date_extraction = offre.get("dateExtraction")
                date_creation = offre.get("dateCreation").split("T")[0]  # inutile de récupérer l'heure
                date_actualisation = offre.get("dateActualisation").split("T")[0]  # inutile de récupérer l'heure
                nombre_postes = offre.get("nombrePostes")

                # print pour investigation si besoin :
                # print(offre_id, date_extraction, date_creation, date_actualisation, nombre_postes, sep="\n-> ")

                fill_db(
                    db_name="OffreEmploi",
                    attributes_tuple=(
                        "offre_id",
                        "date_extraction",
                        "date_creation",
                        "date_actualisation",
                        "nombre_postes",
                    ),
                    on_conflict_string=("offre_id"),
                )

        # conn.commit()

        #### table "Contrat"

        if fill_table_Contrat:
            print("Écriture de la table Contrat")

            for offre in offres_data:
                offre_id = offre.get("id")

                type_contrat = offre.get("typeContrat")
                type_contrat_libelle = offre.get("typeContratLibelle")
                duree_travail_libelle = offre.get("dureeTravailLibelle")
                duree_travail_libelle_converti = offre.get("dureeTravailLibelleConverti")
                nature_contrat = offre.get("natureContrat")
                salaire_libelle = offre.get("salaire").get("libelle")
                salaire_complement_1 = offre.get("salaire").get("complement1")
                salaire_complement_2 = offre.get("salaire").get("complement2")
                salaire_commentaire = offre.get("salaire").get("commentaire")
                alternance = offre.get("alternance")
                deplacement_code = offre.get("deplacementCode")
                deplacement_libelle = offre.get("deplacementLibelle")
                temps_travail = offre.get("complementExercice")
                condition_specifique = offre.get("conditionExercice")

                # print pour investigation si besoin :
                # print(
                #     offre_id, type_contrat, type_contrat_libelle, duree_travail_libelle, duree_travail_libelle_converti, nature_contrat,
                #     salaire_libelle, salaire_complement_1, salaire_complement_2, salaire_commentaire,
                #     alternance, deplacement_code, deplacement_libelle, temps_travail, condition_specifique,
                #     sep="\n-> ",
                # )  # fmt:off

                fill_db(
                    db_name="Contrat",
                    attributes_tuple=(
                        "offre_id",
                        "type_contrat",
                        "type_contrat_libelle",
                        "duree_travail_libelle",
                        "duree_travail_libelle_converti",
                        "nature_contrat",
                        "salaire_libelle",
                        "salaire_complement_1",
                        "salaire_complement_2",
                        "salaire_commentaire",
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
            print("Écriture de la table Entreprise")

            for offre in offres_data:
                offre_id = offre.get("id")

                nom_entreprise = offre.get("entreprise").get("nom")
                description_entreprise = offre.get("entreprise").get("description")
                code_naf = offre.get("codeNAF")
                secteur_activite_libelle = offre.get("secteurActiviteLibelle")
                entreprise_adaptee = offre.get("entreprise").get("entrepriseAdaptee")

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
            print("Écriture de la table Localisation")

            for offre in offres_data:
                offre_id = offre.get("id")

                code_insee = offre.get("code_insee")
                nom_commune = offre.get("nom_commune")
                code_postal = offre.get("code_postal")
                nom_ville = offre.get("nom_ville")
                code_departement = offre.get("code_departement")
                nom_departement = offre.get("nom_departement")
                code_region = offre.get("code_region")
                nom_region = offre.get("nom_region")
                lieu_cas = offre.get("lieu_cas")

                # print pour investigation si besoin :
                # print(offre_id, code_insee, nom_commune, code_postal, nom_ville, code_departement, nom_departement, code_region, nom_region, lieu_cas, sep="\n-> ")

                fill_db(
                    db_name="Localisation",
                    attributes_tuple=(
                        "offre_id",
                        "code_insee",
                        "nom_commune",
                        "code_postal",
                        "nom_ville",
                        "code_departement",
                        "nom_departement",
                        "code_region",
                        "nom_region",
                    ),
                    on_conflict_string=("offre_id"),
                )

        #### table "DescriptionOffre"
        if fill_table_DescriptionOffre:
            print("Écriture de la table DescriptionOffre")

            for offre in offres_data:
                offre_id = offre.get("id")

                intitule_offre = offre.get("intitule")
                description_offre = offre.get("description")
                nom_partenaire = offre.get("origineOffre").get("partenaires", [{}])[0].get("nom")
                rome_code = offre.get("romeCode")
                rome_libelle = offre.get("romeLibelle")
                appellation_rome = offre.get("appellationlibelle")
                difficile_a_pourvoir = offre.get("offresManqueCandidats")
                accessible_travailleurs_handicapes = offre.get("accessibleTH")

                # print pour investigation si besoin :
                # print(offre_id, intitule_offre, description_offre, nom_partenaire, rome_code, rome_libelle, appellation_rome, difficile_a_pourvoir, accessible_travailleurs_handicapes, sep="\n-> ")

                fill_db(
                    db_name="DescriptionOffre",
                    attributes_tuple=(
                        "offre_id",
                        "intitule_offre",
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

        #### table "Competence"
        if fill_table_Competence:
            print("Écriture de la table Competence")

            for offre in offres_data:
                offre_id = offre.get("id")

                competences = offre.get("competences")  # ⛔ Attention on a une liste de compétences dans le json !!!

                if competences:
                    for i in range(len(competences)):
                        # /!\ note : il faut remplacer NULL par quelque chose (cas "competence_code = null")
                        # /!\  (sinon risque d'écriture de doublon car "NULL != NULL selon la logique SQL")
                        # /!\ à la suite de la boucle, on remplacera ces nouvelles valeurs par les "null"
                        competence_code = competences[i].get("code", 0)
                        competence_libelle = competences[i].get("libelle", sql_safe_null)
                        competence_code_exigence = competences[i].get("exigence", sql_safe_null)

                        # print pour investigation si besoin :
                        # print(offre_id, competences, competence_code, competence_libelle, competence_code_exigence, sep="\n-> ", end="\n\n")

                        fill_db(
                            db_name="Competence",
                            attributes_tuple=(
                                "competence_code",
                                "competence_libelle",
                                "competence_code_exigence",
                            ),
                            on_conflict_string=("competence_code | competence_libelle | competence_code_exigence"),
                        )

        #### table "Experience"
        if fill_table_Experience:
            print("Écriture de la table Experience")

            for offre in offres_data:
                offre_id = offre.get("id")

                experience_libelle = offre.get("experienceLibelle") or sql_safe_null
                experience_code_exigence = offre.get("experienceExige") or sql_safe_null
                experience_commentaire = offre.get("experienceCommentaire") or sql_safe_null  # parfois experience_commentaire existe bien et a la valeur "null" dans le json

                # print pour investigation si besoin :
                # print(offre_id, experience_libelle, experience_code_exigence, experience_commentaire, sep="\n-> ", end="\n\n")

                if any([i != sql_safe_null for i in [experience_libelle, experience_code_exigence, experience_commentaire]]):
                    fill_db(
                        db_name="Experience",
                        attributes_tuple=(
                            "experience_libelle",
                            "experience_code_exigence",
                            "experience_commentaire",
                        ),
                        on_conflict_string="experience_libelle | experience_code_exigence | experience_commentaire",
                    )

        #### table "Formation"

        if fill_table_Formation:
            print("Écriture de la table Formation")

            for offre in offres_data:
                offre_id = offre.get("id")

                formations = offre.get("formations", [{}])  # ⛔ Attention on a une liste de formations dans le json !!!

                if formations:
                    for i in range(len(formations)):
                        formation_code = formations[i].get("codeFormation", 0)
                        formation_domaine_libelle = formations[i].get("domaineLibelle", sql_safe_null)
                        formation_niveau_libelle = formations[i].get("niveauLibelle", sql_safe_null)
                        formation_commentaire = formations[i].get("commentaire", sql_safe_null)
                        formation_code_exigence = formations[i].get("exigence", sql_safe_null)

                        # print pour investigation si besoin :
                        # print(offre_id, formations[i], formation_code, formation_domaine_libelle, formation_niveau_libelle, formation_commentaire, formation_code_exigence, sep="\n-> ", end="\n\n")

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

        #### table "QualiteProfessionnelle"

        if fill_table_QualiteProfessionnelle:
            print("Écriture de la table QualiteProfessionnelle")

            for offre in offres_data:
                offre_id = offre.get("id")

                qualites = offre.get("qualitesProfessionnelles")  # ⛔ Attention on a une liste de qualités professionnelles dans le json !!!

                if qualites:  # car on peut avoir dans le json "qualitesProfessionnelles": null
                    for i in range(len(qualites)):
                        qualite_professionnelle_libelle = qualites[i].get("libelle")
                        qualite_professionnelle_description = qualites[i].get("description")

                        # print pour investigation si besoin :
                        # print(offre_id, qualites, qualite_professionnelle_libelle, qualite_professionnelle_description, sep="\n-> ", end="\n\n")

                        fill_db(
                            db_name="QualiteProfessionnelle",
                            attributes_tuple=(
                                "qualite_professionnelle_libelle",
                                "qualite_professionnelle_description",
                            ),
                            on_conflict_string=("qualite_professionnelle_libelle | qualite_professionnelle_description"),
                        )

        #### table "Qualification"

        if fill_table_Qualification:
            print("Écriture de la table Qualification")

            for offre in offres_data:
                offre_id = offre.get("id")

                qualification_code = offre.get("qualificationCode")
                qualification_libelle = offre.get("qualificationLibelle")

                # print pour investigation si besoin :
                # print(offre_id, qualification_code, qualification_libelle, sep="\n-> ", end="\n\n")

                if (qualification_code is not None) or (qualification_libelle is not None):
                    fill_db(
                        db_name="Qualification",
                        attributes_tuple=(
                            "qualification_code",
                            "qualification_libelle",
                        ),
                        on_conflict_string="qualification_code | qualification_libelle",
                    )

                    # cursor.execute(
                    #     f"""--sql
                    #         INSERT INTO Qualification (qualification_code, qualification_libelle)
                    #         VALUES (%s, %s)
                    #         ON CONFLICT (qualification_code, qualification_libelle) DO UPDATE SET
                    #             qualification_code = EXCLUDED.qualification_code,
                    #             qualification_libelle = EXCLUDED.qualification_libelle
                    #         """,
                    #     (qualification_code, qualification_libelle),
                    # )

                    # conn.commit()  # Commit des changements

        #### table "Langue"

        if fill_table_Langue:
            print("Écriture de la table Langue")

            for offre in offres_data:
                offre_id = offre.get("id")

                langues = offre.get("langues")  # ⛔ Attention on a une liste de langues dans le json !!!

                # print pour investigation si besoin :
                # print(offre_id, langues, sep="\n-> ", end="\n\n")

                if langues:
                    for i in range(len(langues)):
                        langue_libelle = langues[i].get("libelle")
                        langue_code_exigence = langues[i].get("exigence")

                        # print pour investigation si besoin :
                        # print(offre_id, langues[i], langue_libelle, langue_code_exigence, sep="\n-> ", end="\n\n")

                        fill_db(
                            db_name="Langue",
                            attributes_tuple=(
                                "langue_libelle",
                                "langue_code_exigence",
                            ),
                            on_conflict_string=("langue_libelle | langue_code_exigence"),
                        )

        #### table "PermisConduire"

        if fill_table_PermisConduire:
            print("Écriture de la table PermisConduire")

            for offre in offres_data:
                offre_id = offre.get("id")

                permisconduires = offre.get("permis")  # ⛔ Attention on a une liste de permisconduires dans le json !!!

                # print pour investigation si besoin :
                # print(offre_id, permisconduires, sep="\n-> ", end="\n\n")

                if permisconduires:
                    for i in range(len(permisconduires)):
                        permis_libelle = permisconduires[i].get("libelle")
                        permis_code_exigence = permisconduires[i].get("exigence")

                        # print pour investigation si besoin :
                        # print(offre_id, permisconduires[i], permis_libelle, permis_code_exigence, sep="\n-> ", end="\n\n")

                        fill_db(
                            db_name="PermisConduire",
                            attributes_tuple=(
                                "permis_libelle",
                                "permis_code_exigence",
                            ),
                            on_conflict_string=("permis_libelle | permis_code_exigence"),
                        )

        ##################
        #### PARTIE 2 ####
        ##################

        if 1:
            """
            Ici, on réécrit les tables où on a dû écrire en base les valeurs différentes de "null" pour éviter d'écrire des doublons.
            (avec la variable "value_not_existing_in_json")
            """

            #### table "Competence"

            if fill_table_Competence:
                print("Mise à jour de la table Competence (on réécrit les NULL)")

                update_query = f"""
                    UPDATE Competence
                    SET
                        competence_code = NULLIF(competence_code, 0),
                        competence_libelle = NULLIF(competence_libelle, '{sql_safe_null}'),
                        competence_code_exigence = NULLIF(competence_code_exigence, '{sql_safe_null}')
                    WHERE
                        competence_code = 0 OR
                        competence_libelle = '{sql_safe_null}' OR
                        competence_code_exigence = '{sql_safe_null}'
                """
                cursor.execute(update_query)
                # conn.commit()

            #### table "Experience"

            if fill_table_Experience:
                print("Mise à jour de la table Experience (on réécrit les NULL)")

                update_query = f"""
                    UPDATE Experience
                    SET
                        experience_libelle = NULLIF(experience_libelle, '{sql_safe_null}'),
                        experience_code_exigence = NULLIF(experience_code_exigence, '{sql_safe_null}'),
                        experience_commentaire = NULLIF(experience_commentaire, '{sql_safe_null}')
                    WHERE
                        experience_libelle = '{sql_safe_null}' OR
                        experience_code_exigence = '{sql_safe_null}' OR
                        experience_commentaire = '{sql_safe_null}'
                """

                cursor.execute(update_query)
                # conn.commit()

            #### table "Formation"

            if fill_table_Formation:
                print("Mise à jour de la table Formation (on réécrit les NULL)")

                update_query = f"""
                    UPDATE Formation
                    SET
                        formation_code = NULLIF(formation_code, 0),
                        formation_domaine_libelle = NULLIF(formation_domaine_libelle, '{sql_safe_null}'),
                        formation_niveau_libelle = NULLIF(formation_niveau_libelle, '{sql_safe_null}'),
                        formation_commentaire = NULLIF(formation_commentaire, '{sql_safe_null}'),
                        formation_code_exigence = NULLIF(formation_code_exigence, '{sql_safe_null}')
                    WHERE
                        formation_code = 0 OR
                        formation_domaine_libelle = '{sql_safe_null}' OR
                        formation_niveau_libelle = '{sql_safe_null}' OR
                        formation_commentaire = '{sql_safe_null}' OR
                        formation_code_exigence = '{sql_safe_null}'
                """

                cursor.execute(update_query)
                # conn.commit()

            #### table "QualiteProfessionnelle"

            if fill_table_QualiteProfessionnelle:
                print("Mise à jour de la table QualiteProfessionnelle (on réécrit les NULL)")
                pass  # pas besoin, on n'a pas de NULL

            #### table "Qualification" : inutile de le faire car toutes les clés ont "NOT NULL" dans le CREATE TABLE
            #### table "Langue" : inutile de le faire car toutes les clés ont "NOT NULL" dans le CREATE TABLE
            #### table "PermisConduire" : inutile de le faire car toutes les clés ont "NOT NULL" dans le CREATE TABLE
        # conn.commit()

        ##################
        #### PARTIE 3 ####
        ##################

        if 1:
            """
            Ici, on s'occupe des tables de liaison, une fois que les tables de dimension associées ont bien les valeurs remplacées par null.

            Explication pour la suite de `(competence_code IS NULL AND %s IS NULL OR competence_code = %s)` :

              - Partie 1 : `competence_code IS NULL AND %s IS NULL`
                - Si competence_code est NULL et si la valeur passée en paramètre est aussi NULL, alors la condition est vraie.

              - Partie 2 : `competence_code = %s`
                - Si competence_code est égal à la valeur passée en paramètre (c'est-à-dire, non NULL et identique), la condition est vraie.

              - Ainsi, cette condition permet de gérer le cas où la valeur NULL doit être traitée de manière spécifique.
                (puisque NULL n'est jamais égal à NULL en SQL, il faut une vérification explicite)

            """

            #### table "Offre_Competence"

            if fill_table_Offre_Competence:
                print("Écriture de la table Offre_Competence")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    competences = offre.get("competences")  # ⛔ Attention on a une liste de compétences dans le json !!!

                    if competences:
                        for i in range(len(competences)):
                            competence_code = competences[i].get("code")
                            competence_libelle = competences[i].get("libelle")
                            competence_code_exigence = competences[i].get("exigence")

                            # print pour investigation si besoin :
                            # print(offre_id, competence_code, competence_libelle, competence_code_exigence, sep="\n-> ")

                            # Récupérer competence_id
                            query = """
                                SELECT competence_id
                                FROM Competence
                                WHERE
                                    (competence_code IS NULL AND %s IS NULL OR competence_code = %s)
                                    AND (competence_libelle IS NULL AND %s IS NULL OR competence_libelle = %s)
                                    AND (competence_code_exigence IS NULL AND %s IS NULL OR competence_code_exigence = %s)
                            """
                            cursor.execute(
                                query,
                                (competence_code, competence_code, competence_libelle, competence_libelle, competence_code_exigence, competence_code_exigence),
                            )

                            competence_id = cursor.fetchone()[0]

                            # print pour investigation si besoin :
                            # print(offre_id, competence_code, competence_libelle, competence_code_exigence, competence_id, sep="\n-> ")

                            fill_db(
                                db_name="Offre_Competence",
                                attributes_tuple=(
                                    "offre_id",
                                    "competence_id",
                                ),
                                on_conflict_string="offre_id | competence_id",
                            )

            #### table "Offre_Experience"

            if fill_table_Offre_Experience:
                print("Écriture de la table Offre_Experience")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    experience_libelle = offre.get("experienceLibelle")
                    experience_code_exigence = offre.get("experienceExige")
                    experience_commentaire = offre.get("experienceCommentaire")

                    # Récupérer experience_id
                    query = """
                        SELECT experience_id
                        FROM Experience
                        WHERE
                            (experience_libelle IS NULL AND %s IS NULL OR experience_libelle = %s)
                            AND (experience_code_exigence IS NULL AND %s IS NULL OR experience_code_exigence = %s)
                            AND (experience_commentaire IS NULL AND %s IS NULL OR experience_commentaire = %s)
                    """

                    # print pour investigation si besoin :
                    # print(offre_id, experience_libelle, experience_code_exigence, experience_commentaire, sep="\n-> ")

                    cursor.execute(query, (experience_libelle, experience_libelle, experience_code_exigence, experience_code_exigence, experience_commentaire, experience_commentaire))
                    experience_id = cursor.fetchone()[0]

                    fill_db(
                        db_name="Offre_Experience",
                        attributes_tuple=(
                            "offre_id",
                            "experience_id",
                        ),
                        on_conflict_string="offre_id | experience_id",
                    )

            #### table "Offre_Formation"

            if fill_table_Offre_Formation:
                print("Écriture de la table Offre_Formation")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    formations = offre.get("formations", [{}])  # ⛔ Attention on a une liste de formations dans le json !!!

                    if formations:
                        for i in range(len(formations)):
                            formation_code = formations[i].get("codeFormation")
                            formation_domaine_libelle = formations[i].get("domaineLibelle")
                            formation_niveau_libelle = formations[i].get("niveauLibelle")
                            formation_commentaire = formations[i].get("commentaire")
                            formation_code_exigence = formations[i].get("exigence")

                            # Récupérer formation_id
                            query = """
                                SELECT formation_id
                                FROM Formation
                                WHERE
                                    (formation_code IS NULL AND %s IS NULL OR formation_code = %s)
                                    AND (formation_domaine_libelle IS NULL AND %s IS NULL OR formation_domaine_libelle = %s)
                                    AND (formation_niveau_libelle IS NULL AND %s IS NULL OR formation_niveau_libelle = %s)
                                    AND (formation_commentaire IS NULL AND %s IS NULL OR formation_commentaire = %s)
                                    AND (formation_code_exigence IS NULL AND %s IS NULL OR formation_code_exigence = %s)
                            """

                            cursor.execute(
                                query,
                                (
                                    formation_code, formation_code,
                                    formation_domaine_libelle, formation_domaine_libelle,
                                    formation_niveau_libelle, formation_niveau_libelle,
                                    formation_commentaire, formation_commentaire,
                                    formation_code_exigence, formation_code_exigence,
                                ),
                            )  # fmt: off

                            formation_id = cursor.fetchone()[0]

                            # print pour investigation si besoin :
                            # print(offre_id, formation_code, formation_domaine_libelle, formation_niveau_libelle,
                            #     formation_commentaire, formation_code_exigence, formation_id, sep="\n-> ", end="\n\n")  # fmt: off

                            fill_db(
                                db_name="Offre_Formation",
                                attributes_tuple=(
                                    "offre_id",
                                    "formation_id",
                                ),
                                on_conflict_string="offre_id | formation_id",
                            )

            #### table "Offre_QualiteProfessionnelle"

            if fill_table_Offre_QualiteProfessionnelle:
                print("Écriture de la table Offre_QualiteProfessionnelle")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    qualites = offre.get("qualitesProfessionnelles")  # ⛔ Attention on a une liste de qualités professionnelles dans le json !!!

                    if qualites:  # car on peut avoir dans le json "qualitesProfessionnelles": null
                        for i in range(len(qualites)):
                            qualite_professionnelle_libelle = qualites[i].get("libelle")
                            qualite_professionnelle_description = qualites[i].get("description")

                            query = "WHERE qualite_professionnelle_libelle = %s AND qualite_professionnelle_description = %s"

                            # Récupérer qualite_professionnelle_id
                            query = """
                                SELECT qualite_professionnelle_id
                                FROM QualiteProfessionnelle
                                WHERE
                                    (qualite_professionnelle_libelle IS NULL AND %s IS NULL OR qualite_professionnelle_libelle = %s)
                                    AND (qualite_professionnelle_description IS NULL AND %s IS NULL OR qualite_professionnelle_description = %s)
                            """

                            cursor.execute(query, (qualite_professionnelle_libelle, qualite_professionnelle_libelle, qualite_professionnelle_description, qualite_professionnelle_description))
                            qualite_professionnelle_id = cursor.fetchone()[0]

                            fill_db(
                                db_name="Offre_QualiteProfessionnelle",
                                attributes_tuple=(
                                    "offre_id",
                                    "qualite_professionnelle_id",
                                ),
                                on_conflict_string="offre_id | qualite_professionnelle_id",
                            )

            #### table "Offre_Qualification"

            if fill_table_Offre_Qualification:
                print("Écriture de la table Offre_Qualification")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    qualification_code = offre.get("qualificationCode")
                    qualification_libelle = offre.get("qualificationLibelle")
                    date_extraction = offre.get("dateExtraction")

                    # print pour investigation si besoin :
                    # print(offre_id, qualification_code, qualification_libelle, sep="\n-->", end="\n\n")

                    if (qualification_code is not None) and (qualification_libelle is not None):
                        # récupérer qualification_code
                        query = """
                            SELECT qualification_code
                            FROM Qualification
                            WHERE
                                (qualification_code IS NULL AND %s IS NULL OR qualification_code = %s)
                                AND (qualification_libelle IS NULL AND %s IS NULL OR qualification_libelle = %s)
                        """

                        cursor.execute(query, (qualification_code, qualification_code, qualification_libelle, qualification_libelle))
                        qualification_code = cursor.fetchone()[0]

                        # print pour investigation si besoin :
                        # print(offre_id, qualification_code, qualification_libelle, sep="\n-->", end="\n\n")

                        fill_db(
                            db_name="Offre_Qualification",
                            # attributes_tuple=("offre_id", "qualite_professionnelle_id"),
                            # on_conflict_string="offre_id | qualite_professionnelle_id",
                            attributes_tuple=(
                                "offre_id",
                                "qualification_code",
                                "date_extraction",
                            ),
                            on_conflict_string="offre_id | qualification_code",
                        )

                        # cursor.execute(
                        #     f"""--sql
                        #         INSERT INTO Offre_Qualification (offre_id, qualification_code, date_extraction)
                        #         VALUES (%s, %s, %s)
                        #         -- ON CONFLICT (offre_id) DO UPDATE SET
                        #         ON CONFLICT (offre_id, qualification_code) DO UPDATE SET
                        #             -- qualification_code = EXCLUDED.qualification_code,
                        #             date_extraction = EXCLUDED.date_extraction
                        #         """,
                        #     (offre_id, qualification_code, date_extraction),
                        # )

                        # conn.commit()

                # On supprime les lignes où 1 offre_id est présente avec 2 qualification_code différents :
                cursor.execute(f"""--sql
                    -- CTE pour afficher l'offre_id le plus récent
                    --  s'il y a 1 offre_id avec plusieurs qualification_code
                    WITH latest_offre_id AS (
                        SELECT DISTINCT ON (offre_id)
                            offre_id,
                            qualification_code,
                            date_extraction
                        FROM offre_qualification
                        ORDER BY offre_id, date_extraction DESC
                    )
                    DELETE FROM offre_qualification
                    WHERE (offre_id, qualification_code, date_extraction) NOT IN (
                        SELECT offre_id, qualification_code, date_extraction
                        FROM latest_offre_id
                    );
                    """)

                # conn.commit()

                # fill_db(
                #     db_name="Offre_Qualification",
                #     attributes_tuple=("offre_id", "qualification_code"),
                #     on_conflict_string="offre_id | qualification_code",
                # )

            #### table "Offre_Langue"

            if fill_table_Offre_Langue:
                print("Écriture de la table Offre_Langue")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    langues = offre.get("langues")  # ⛔ Attention on a une liste de langues dans le json !!!

                    # print pour investigation si besoin :
                    # print(offre_id, langues, sep="\n-> ", end="\n\n")

                    if langues:
                        for i in range(len(langues)):
                            langue_libelle = langues[i].get("libelle")
                            langue_code_exigence = langues[i].get("exigence")

                            # Récupérer langue_id
                            query = """
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

            #### table "Offre_PermisConduire"

            if fill_table_Offre_PermisConduire:
                print("Écriture de la table Offre_PermisConduire")

                for offre in offres_data:
                    offre_id = offre.get("id")

                    permisconduires = offre.get("permis")  # ⛔ Attention on a une liste de permisconduires dans le json !!!

                    if permisconduires:
                        for i in range(len(permisconduires)):
                            permis_libelle = permisconduires[i].get("libelle")
                            permis_code_exigence = permisconduires[i].get("exigence")

                            # Récupérer permis_id
                            query = """
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
