- Ces fichiers pgsql sont destinés à être exécutés depuis le sript Python `Job_Market/fastapi/fastapi.py` (avec notamment psycopg2).

- Les placeholders seront remplacés dynamiquement par les variables dans le script Python.

- Sinon on peut hardcoder les valeurs dans le cas où on veut exécuter ce script SQL directement (sans script Python), par exemple :

  - metier_data = 'DE', 'DA' ou 'DS'
  - date_creation >= '2025-04-10'
  - code_region = 11 (pour l'Île-de-France)
  - nom_region = 'Île-de-France'
  - code_departement = 78
  - nom_departement = 'Yvelines'
  - code_postal = 78000
  - nom_ville = 'Versailles'
