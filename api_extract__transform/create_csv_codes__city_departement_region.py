import os

import pandas as pd

# todo : ajouter la partie download / unzip des fichiers (pas urgent)


# Fichiers du lien_2
# ==================

current_directory = os.path.dirname(os.path.abspath(__file__))

files_directory = os.path.join(
    current_directory,
    "..",
    "additional_files",
    "archives",
)
file_commune = "v_commune_2024.csv"
file_departement = "v_departement_2024.csv"
file_region = "v_region_2024.csv"


# df_commune
# ==========

df_commune = pd.read_csv(
    os.path.join(files_directory, "lien_2", file_commune),
    usecols=[
        "COM",
        "REG",
        "DEP",
        "LIBELLE",
    ],
)


df_commune.rename(
    {
        "COM": "code_insee",
        "REG": "code_region",
        "DEP": "code_departement",
        "LIBELLE": "nom_commune",
    },
    axis=1,
    inplace=True,
)


# On ajoute une colonne nom_ville (idem que nom_commune sans les arrondissements pour Paris, Marseille et Lyon)
#  car on va préférer "Lyon" à "Lyon 1er Arrondissement" ou "Lyon 2e Arrondissement"...

df_commune["nom_ville"] = df_commune.apply(
    lambda x: x.nom_commune.split(" ")[0] if "Arrondissement" in x.nom_commune else x.nom_commune,
    axis=1,
)


df_departement = pd.read_csv(
    os.path.join(files_directory, "lien_2", file_departement),
    usecols=["DEP", "LIBELLE"],
)


df_departement.rename(
    {"DEP": "code_departement", "LIBELLE": "nom_departement"},
    axis=1,
    inplace=True,
)


df_region = pd.read_csv(
    os.path.join(files_directory, "lien_2", file_region),
    usecols=["REG", "LIBELLE"],
)


df_region.rename(
    {"REG": "code_region", "LIBELLE": "nom_region"},
    axis=1,
    inplace=True,
)


# merging

df_lien_2 = df_commune.merge(df_departement, on="code_departement").merge(df_region, on="code_region")


# pour avoir code_region = 84 au lieu de 84.0 par exemple
df_lien_2.code_region = df_lien_2.code_region.astype(int).astype(str)

df_lien_2 = df_lien_2[
    [
        "code_insee",
        "nom_commune",
        "nom_ville",
        "code_departement",
        "nom_departement",
        "code_region",
        "nom_region",
    ]
]


# Fichier du lien_3
# =================

# Mapping code insee <> code postal

df_lien_3 = pd.read_csv(
    os.path.join(files_directory, "lien_3", "cities.csv"),
    usecols=["insee_code", "zip_code"],
)


df_lien_3.rename(
    {"insee_code": "code_insee", "zip_code": "code_postal"},
    axis=1,
    inplace=True,
)


df_lien_3[df_lien_3.code_insee == "75056"]  # non disponible dans ce fichier, donc attention au merge


df_lien_3["code_postal"] = df_lien_3["code_postal"].astype(str)


# Merge des df des liens 2 et 3
# =============================

df = pd.merge(left=df_lien_2, right=df_lien_3, on="code_insee", how="left")
# left car tous les code_insee ne sont pas disponibles dans df_lien_3

df = df[
    [
        "code_insee",
        "nom_commune",
        "code_postal",
        "nom_ville",
        "code_departement",
        "nom_departement",
        "code_region",
        "nom_region",
    ]
]


df["code_postal"] = df["code_postal"].str.zfill(5)


df = df.drop_duplicates(["code_insee", "code_postal"])


# Ecriture dans un fichier .csv
# =============================

df.to_csv(
    os.path.join(
        current_directory,
        "..",
        "additional_files",
        "codes__city_department_region.csv",
    ),
    index=False,  # pour ne pas écrire les index
)


df_merge = pd.read_csv(
    os.path.join(
        current_directory,
        "..",
        "additional_files",
        "codes__city_department_region.csv",
    ),
    dtype=str,
)
