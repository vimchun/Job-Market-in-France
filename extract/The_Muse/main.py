import json
import os
import sys

import requests

# url params variables
api_key = ""  # À compléter après (pas obligatoire, on aura juste moins de requêtes possible)
page = 0  # The page number to load (required)  [20 résultats par page]
descending = "false"  # Whether to show descending results (allowed values: true or false, defaults to false)
company = ""  # Only get jobs for these companies
category = [  # The job category to get
    "Data and Analytics",
    "Data Science",
    "Science and Engineering",
]
level = [  # The experience level required for the job
    "Entry Level",
    "Mid Level",
    "Senior Level",
    "management",
    "Internship",
]
location = [  # The job location to get (you can include flexible/remote jobs from here)
    # "Zvolen, Slovakia"  # location=Zvolen%2C%20Slovakia
    # à remplir pour toutes les villes françaises
]


# Traitement pour avoir les paramètres "category", "level" formatés de la manière attendue

categories = "&".join([f'category={cat.replace(" ", "%20")}' for cat in category])
# print(categories)  ##==> permet d'avoir par exemple : category=Data%20and%20Analytics&category=Data%20Science&category=Science%20and%20Engineering

levels = "&".join([f'level={lvl.replace(" ", "%20")}' for lvl in level])
# print(levels) ##==> permet d'avoir par exemple : level=Entry%20Level&level=Mid%20Level&level=Senior%20Level&level=management&level=Internship


# requête pour voir combien d'offres on a en tout (clé "total"), et surtout pour savoir combien de requêtes sont nécessaires (clé "page_count")
url_init = (
    f"https://www.themuse.com/api/public/jobs?"
    f"page={page}&"
    # f"api_key={api_key}&"
    f"descending={descending}&"
    f"{categories}&"
    f"{levels}&"
    f"location=Paris%2C%20France"
    )  # fmt: skip


response = requests.get(url_init)

if response.status_code == 200:
    print(f"Status Code: {response.status_code}\n")
    data = response.json()
    # print(data)
    nombre_requete_total = data["page_count"]
    print(f"Il faut faire {nombre_requete_total} requêtes pour avoir les {data["total"]} offres.\n")

else:
    print(f"Erreur lors de la requête API: {response.status_code}\n")
    print(response.text)


# Maintenant qu'on sait combien de requêtes sont nécessaires au total, on prépare la boucle for

url_sans_page = (  # sans paramètre "page" car il sera paramétré dans la boucle for ci-après
    f"https://www.themuse.com/api/public/jobs?"
    # f"api_key={api_key}&"
    f"descending={descending}&"
    f"{categories}&"
    f"{levels}&"
    # f"location=Abbeville%2C%20France"
    f"location=Paris%2C%20France"
    )  # fmt: skip

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "outputs", "output.json")
if os.path.exists(file_path):
    os.remove(file_path)

for page in range(nombre_requete_total):
    url = (
        f"{url_sans_page}"
        f"&page={page}"
        )  # fmt: skip

    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Status Code: {response.status_code}\n")

        data = response.json()
        # print(data)
        with open(file_path, "a", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Erreur lors de la requête API: {response.status_code}\n")
        print(response.text)

# todo : supprimer les offres en remote ? sûrement à faire...
