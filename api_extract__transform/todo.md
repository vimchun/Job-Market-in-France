todo (ou pas)

# 0/ Supprimer les offres DOMTOM et Corse


# 1/ Extraire la ville, la commune, le département, et la région


Le faire depuis l'attribut "Description Lieu" ou depuis l'attribut "Intitule" quand l'information n'est pas présente dans les attributs "Code Postal" ou "Code Commune"

(note : possible de récupérer l'information depuis les coordonnées GPS ? cf geopy ? sachant que certaines coordonnées gps sont erronées, comme vu avec power bi : Rouen en Allemagne, Annecy en Somalie)

En effet, parfois :
 - Une offre n'a ni le "Code Postal", ni le "Code Commune" renseigné mais "Description Lieu" renseigné
   - Exemple : l'offre 0526013 a "Code Postal = null" et "Code Commune = null", mais elle a "Description Lieu = 95 - Val d'Oise"
 - Une offre n'a ni le "Code Postal", ni le "Code Commune" renseigné et "Description Lieu = France", mais l'information peut être dans l'intitulé
   - Exemple : l'offre 9598734 est en IDF ("Intitulé Offre : Data Engineer PySpark - Data Factory - Services Financiers - Ile de France (H/F)")


# 2/ Ajouter un attribut pour savoir si l'offre est encore d'actualité ou pas
