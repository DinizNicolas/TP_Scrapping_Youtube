# TP_Scrapping_Youtube

Pour modifier les vidéos scrappées, il faut supprimer ou ajouter des valeurs dans la liste dans le fichier input.json.

Commandes pour lancer le script
  python3.8 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  python scrapper.py --input input.json --output output.json
  
Commande pour faire les tests
  python -m pytest tests
  
Commande pour faire le calcul du coverage
  pytest --cov=. tests/
