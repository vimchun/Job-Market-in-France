Problèmes vus sur Power BI :

# Localisation

## Certains code postaux sont mal placés sur la carte Bing

Par exemple, le code postal 97100 (Guadeloupe) est placé en Indonésie.


### Solution

En fait, on ne veut que les offres qui sont en France Métropolitaine.

La colonne "Description Lieu" peut prendre plusieurs formes :
  - [numéro département] - [nom ville] (arrondissement)    <== dans la plupart des cas
  - [numéro département]
  - [région]
  - [pays]
  - [ville]
  - [départements et régions d'outre-mer]


On va créer une colonne "France Métropolitaine" de type booléen dans PQ, qui vaudra :
  - False si la colonne "Description Lieu" :
    - commence avec 2 digits parmi ["2A", "2B"] (Corse)
    - commence avec 3 digits parmi ["971", "972", "973", "974", "976", "987", "988"] (DOM-TOM)
    - a une valeur parmi ["Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte"]
  - True sinon

On filtrera sur "France Métropolitaine = True", et on supprimera cette colonne.


  ``` M
  Table.AddColumn(#"Removed Other Columns", "France Métropolitaine", each
      let
          CodeDepartement = Text.Start([Description Lieu], 3),  // Extraire les 3 premiers caractères
          CodeNumerique = Text.Select(CodeDepartement, {"0".."9"}),  // Garder uniquement les chiffres
          EstNumerique = Text.Length(CodeNumerique) = 3,  // Vérifier si la longueur est 3 (c'est un code de département)
          ListeDOM = {"Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte", "Saint-Pierre-et-Miquelon", "La Polynésie française", "Nouvelle Calédonie"},  // Liste des DOM-TOM
          EstDOMTOM = List.Contains(ListeDOM, [Description Lieu]),  // Vérifier si le lieu appartient à la liste DOM-TOM
          EstCorse = Text.Start(CodeDepartement, 2) = "2A" or Text.Start(CodeDepartement, 2) = "2B"  // Vérifier si c'est un département de la Corse
      in
          if EstNumerique and List.Contains({"971", "972", "973", "974", "976", "987", "988"}, CodeDepartement) then
              false  // Si c'est un DOM-TOM (code département à 3 chiffres), mettre False
          else if EstDOMTOM then
              false  // Si le lieu est dans la liste des DOM-TOM, mettre False
          else if EstCorse then
              false  // Si le département est en Corse (2A ou 2B), mettre False
          else
              true)  // Sinon, True pour la France Métropolitaine
  ```

Exemple de valeurs de la colonne "Description Lieu" :
  13
  13 - AIX EN PROVENCE
  75
  75 - Paris (Dept.)
  75 - PARIS 09
  78 - RAMBOUILLET
  971 - Guadeloupe
  972 - LE LAMENTIN
  974 - ST DENIS
  976 - MAMOUDZOU
  Centre-Val de Loire
  France
  Ile-de-France
  La Réunion
  Martinique
  Paris


### Rappel

- France Métropolitaine :
  Les départements métropolitains ont 2 chiffres, de 01 à 95.

- DOM-TOM (Départements et Territoires d'Outre-Mer) :
  Les départements et régions d'outre-mer (DOM) ainsi que les collectivités d'outre-mer (COM) ont un numéro à 3 chiffres.

  Exemple :
    971 pour la Guadeloupe
    972 pour la Martinique
    973 pour la Guyane
    974 pour La Réunion
    976 pour Mayotte
    n numéro à 3 chiffres.


## Certaines coordonnées GPS ne sont pas correctes

Exemples :
- Rouen en Allemagne
- Annecy en Somalie


### Solution

On supprime les colonnes "Latitude" et "Longitude", car certaines d'entre elles ne sont pas bien renseignées au niveau de l'API, et elles n'apportent pas vraiment d'intérêt (le code postal suffit pour la dataviz).