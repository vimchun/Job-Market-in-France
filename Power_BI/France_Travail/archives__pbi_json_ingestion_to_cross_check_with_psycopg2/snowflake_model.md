# Table de fait

## Offre Emploi
- clé : "Offre ID"
  --
  - "Date Création"
  - "Date Actualisation"
  - "Nombre Postes"


# Table de dimension

## Description Offre
- clé : "Offre ID"
  --
  - "Intitule Offre"
  - "Description Offre"
  - "Nom Partenaire"
  - "ROME Code"
  - "ROME Libellé"
  - "Appellation ROME"
  - "Difficile A Pourvoir"
  - "Accessible Travailleurs Handicapés"


## Contrat
- clé : "Offre ID"
  --
  - "Type Contrat"
  - "Type Contrat Libellé"
  - "Durée Travail Libellé"
  - "Durée Travail Libellé Converti"
  - "Salaire Commentaire"
  - "Salaire Libellé"
  - "Salaire Complément 1"
  - "Salaire Complément 2"
  - "Nature Contrat"
  - "Alternance"
  - "Déplacement Code"
  - "Déplacement Libellé"
  - "Temps Travail"
  - "Condition Spécifique"


## Entreprise
- clé : "Offre ID"
  --
  - "Nom Entreprise"
  - "Description Entreprise"
  - "Entreprise Adaptée"
  - "Code NAF"
  - "Secteur Activité Libellé"


## Localisation
- clé : "Offre ID"
  --
  - "Code Postal"
  - "Code Commune"
  - "Description Lieu"


## Compétence
- clé : "Compétence ID"
  --
  - "Code"
  - "Libellé"
  - "Exigence"


## Expérience
- clé : "Expérience ID"
  --
  - "Libellé"
  - "Exigence"
  - "Commentaire"


## Formation
- clé : "Formation ID"
  --
  - "Libellé"
  - "Exigence"
  - "Code"
  - "Libellé"


## Qualité Professionnelle
- clé : "Qualité ID"
  --
  - "Libellé"
  - "Description"


## Qualification
- clé : "Qualification ID"
  --
  - "Code"
  - "Libellé"


## Langue
- clé : "Langue ID"
  --
  - "Libellé"
  - "Exigence"


## Permis de Conduire
- clé : "Permis ID"
  --
  - "Libellé"
  - "Exigence"


# Tables de liaison

## Offre - Compétence
- clé : "Compétence ID", "Offre ID"


## Offre - Expérience
- clé : "Expérience ID", "Offre ID"


## Offre - Niveau Formation
- clé : "Niveau ID", "Offre ID"


## Offre - Domaine Formation
- clé : "Domaine ID", "Offre ID"


## Offre - Qualité Professionnelle
- clé : "Qualité ID", "Offre ID"


## Offre - Qualification
- clé : "Qualification ID", "Offre ID"


## Offre - Langue
- clé : "Langue ID", "Offre ID"


## Offre - Permis de Conduire
- clé : "Permis ID", "Offre ID"