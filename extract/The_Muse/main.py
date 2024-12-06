import requests
import sys


# url params variables
api_key = ""
page = 1  # The page number to load (required)  [20 résultats par page]
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
    "Zvolen, Slovakia"  # location=Zvolen%2C%20Slovakia
]


# Traitement pour avoir les paramètres "category", "level" formatés de la manière attendue

categories = "&".join([f"category={cat.replace(" ", "%20")}" for cat in category])
# print(categories)  ##==> permet d'avoir par exemple : category=Data%20and%20Analytics&category=Data%20Science&category=Science%20and%20Engineering

levels = "&".join([f"level={lvl.replace(" ", "%20")}" for lvl in level])
# print(levels) ##==> permet d'avoir par exemple : level=Entry%20Level&level=Mid%20Level&level=Senior%20Level&level=management&level=Internship



url = (
    f"https://www.themuse.com/api/public/jobs?"
    # f"api_key={api_key}&"
    f"page={page}&"
    f"descending={descending}&"
    f"{categories}&"
    f"{levels}&"
    # f"location=Abbeville%2C%20France"
    f"location=Paris%2C%20France"
    )  # fmt: skip

print(url)



# sys.exit()

response = requests.get(url)

if response.status_code == 200:
    print(f"Status Code: {response.status_code}\n")
    # print(f"Réponse de l'API: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")
    # ensure_ascii=False sinon on a des caractères non compréhensible (ex: Op\u00e9rateur)

    # file_path = os.path.join(current_directory, "outputs", "appellations", "appellations.json")
    data = response.json()
    print(data)
    # with open(file_path, "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

else:
    print(f"Erreur lors de la requête API: {response.status_code}\n")
    print(response.text)
