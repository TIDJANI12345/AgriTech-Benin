#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py setup_groups

# Peupler la base de données avec des données de test
# Cette commande ne plante pas si les données existent déjà
python manage.py populate_db || echo "Les données existent déjà ou erreur lors du peuplement"