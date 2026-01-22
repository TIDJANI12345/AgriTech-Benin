# 📚 GUIDE DES COMMANDES DJANGO

Guide complet de toutes les commandes utilisées dans le projet AgriTech-Bénin avec explications détaillées.

---

## 🔧 COMMANDES PYTHON & ENVIRONNEMENT

### 1. Vérifier la version de Python
```bash
python --version
```
**ou**
```bash
python3 --version
```
**Rôle :** Affiche la version de Python installée sur votre système  
**Résultat attendu :** `Python 3.x.x` (nous avons Python 3.11.9)

---

### 2. Créer un environnement virtuel
```bash
python -m venv venv
```
**Rôle :** Crée un environnement virtuel Python isolé dans un dossier `venv`  
**Pourquoi ?** 
- Isole les dépendances du projet
- Évite les conflits entre différents projets
- Facilite le déploiement

**Décomposition :**
- `python -m` : Exécute un module Python
- `venv` : Module de création d'environnement virtuel
- `venv` (2ème) : Nom du dossier à créer

---

### 3. Activer l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**Mac/Linux :**
```bash
source venv/bin/activate
```

**Rôle :** Active l'environnement virtuel  
**Résultat visible :** `(venv)` apparaît devant votre ligne de commande  
**Important :** Toutes les installations pip se feront dans cet environnement uniquement

---

### 4. Désactiver l'environnement virtuel
```bash
deactivate
```
**Rôle :** Désactive l'environnement virtuel et revient à l'environnement Python global

---

## 📦 COMMANDES PIP (GESTION DES PACKAGES)

### 5. Installer Django
```bash
pip install django
```
**Rôle :** Installe la dernière version de Django dans l'environnement virtuel  
**Ce qui est installé :** Django + toutes ses dépendances  
**Version installée :** Django 5.2.10 (dans notre cas)

---

### 6. Vérifier les packages installés
```bash
pip list
```
**Rôle :** Affiche tous les packages Python installés dans l'environnement actuel

---

### 7. Installer depuis requirements.txt
```bash
pip install -r requirements.txt
```
**Rôle :** Installe tous les packages listés dans le fichier requirements.txt  
**Utilité :** Reproduire exactement le même environnement sur une autre machine

---

### 8. Créer un fichier requirements.txt
```bash
pip freeze > requirements.txt
```
**Rôle :** Exporte la liste de tous les packages installés avec leurs versions exactes  
**Utilité :** Partager les dépendances du projet avec d'autres développeurs

---

## 🚀 COMMANDES DJANGO-ADMIN (CRÉATION DE PROJET)

### 9. Vérifier la version de Django
```bash
django-admin --version
```
**Rôle :** Affiche la version de Django installée  
**Résultat :** `5.2.10` (dans notre cas)

---

### 10. Créer un nouveau projet Django
```bash
django-admin startproject nom_projet .
```
**Exemple utilisé :**
```bash
django-admin startproject agritech .
```

**Rôle :** Crée la structure de base d'un projet Django  

**Structure créée :**
```
agritech/
    __init__.py
    settings.py      # Configuration du projet
    urls.py          # Routes principales
    asgi.py          # Point d'entrée ASGI (async)
    wsgi.py          # Point d'entrée WSGI (production)
manage.py            # Script de gestion du projet
```

**Le point (`.`) à la fin :** Crée le projet dans le dossier actuel (sans créer un sous-dossier supplémentaire)

---

## ⚙️ COMMANDES MANAGE.PY (GESTION DU PROJET)

### 11. Lancer le serveur de développement
```bash
python manage.py runserver
```
**Rôle :** Démarre un serveur web de développement local  
**Accès :** http://127.0.0.1:8000/  
**Options :**
- `python manage.py runserver 8080` : Change le port
- `python manage.py runserver 0.0.0.0:8000` : Rend accessible depuis le réseau

**⚠️ ATTENTION :** À utiliser uniquement en développement, jamais en production !

---

### 12. Créer une nouvelle application Django
```bash
python manage.py startapp nom_app
```
**Exemple utilisé :**
```bash
python manage.py startapp gestion
```

**Rôle :** Crée une nouvelle application Django (composant modulaire du projet)

**Structure créée :**
```
gestion/
    __init__.py
    admin.py         # Configuration interface admin
    apps.py          # Configuration de l'app
    models.py        # Modèles de données (tables)
    tests.py         # Tests unitaires
    views.py         # Logique métier (vues)
    migrations/      # Historique des modifications DB
```

**Différence projet vs app :**
- **Projet** : Configuration globale (agritech)
- **App** : Module fonctionnel réutilisable (gestion)

---

### 13. Créer les migrations
```bash
python manage.py makemigrations
```
**Rôle :** Génère les fichiers de migration à partir des modifications de `models.py`  

**Ce qui se passe :**
1. Django détecte les changements dans vos modèles
2. Crée un fichier Python dans `gestion/migrations/`
3. Ce fichier contient les instructions pour modifier la base de données

**Options utiles :**
- `python manage.py makemigrations gestion` : Migrations pour une app spécifique
- `python manage.py makemigrations --name nom_descriptif` : Donner un nom personnalisé

---

### 14. Appliquer les migrations
```bash
python manage.py migrate
```
**Rôle :** Applique les migrations à la base de données  

**Ce qui se passe :**
1. Django lit tous les fichiers de migration
2. Exécute les commandes SQL nécessaires
3. Crée/modifie les tables dans la base de données
4. Enregistre quelles migrations ont été appliquées

**Options utiles :**
- `python manage.py migrate gestion` : Migrer une app spécifique
- `python manage.py migrate gestion 0001` : Migrer jusqu'à une version spécifique

---

### 15. Afficher l'état des migrations
```bash
python manage.py showmigrations
```
**Rôle :** Affiche toutes les migrations et leur état (appliquée ou non)  
**Symboles :**
- `[X]` : Migration appliquée
- `[ ]` : Migration non appliquée

---

### 16. Afficher le SQL d'une migration
```bash
python manage.py sqlmigrate nom_app numero_migration
```
**Exemple :**
```bash
python manage.py sqlmigrate gestion 0001
```
**Rôle :** Affiche le code SQL qui sera exécuté par une migration  
**Utilité :** Comprendre ce que Django va faire dans la base de données

---

### 17. Créer un superutilisateur (admin)
```bash
python manage.py createsuperuser
```
**Rôle :** Crée un compte administrateur pour accéder à l'interface admin Django

**Questions posées :**
- Username : Nom d'utilisateur
- Email : Email (optionnel)
- Password : Mot de passe (ne s'affiche pas pendant la saisie)

**Accès admin après création :** http://127.0.0.1:8000/admin/

---

### 18. Changer le mot de passe d'un utilisateur
```bash
python manage.py changepassword nom_utilisateur
```
**Rôle :** Modifie le mot de passe d'un utilisateur existant

---

### 19. Ouvrir le shell Django
```bash
python manage.py shell
```
**Rôle :** Ouvre un shell Python interactif avec Django configuré  
**Utilité :**
- Tester des requêtes sur la base de données
- Manipuler les modèles directement
- Déboguer du code

**Exemple d'utilisation :**
```python
from gestion.models import Commune
communes = Commune.objects.all()
print(communes)
```

---

### 20. Vérifier le projet (check)
```bash
python manage.py check
```
**Rôle :** Vérifie que le projet n'a pas d'erreurs de configuration  
**Vérifie :**
- Erreurs dans settings.py
- Problèmes de compatibilité
- Configurations manquantes

---

### 21. Collecter les fichiers statiques
```bash
python manage.py collectstatic
```
**Rôle :** Rassemble tous les fichiers statiques (CSS, JS, images) dans un seul dossier  
**Utilité :** Préparation pour le déploiement en production

---

### 22. Créer une sauvegarde de la base de données
```bash
python manage.py dumpdata > backup.json
```
**Rôle :** Exporte toutes les données de la base dans un fichier JSON  
**Options :**
- `python manage.py dumpdata gestion > backup_gestion.json` : Une app spécifique
- `python manage.py dumpdata --indent 4` : Format lisible avec indentation

---

### 23. Restaurer une sauvegarde
```bash
python manage.py loaddata backup.json
```
**Rôle :** Import des données depuis un fichier JSON dans la base de données

---

### 24. Vider une table
```bash
python manage.py flush
```
**Rôle :** Supprime TOUTES les données de TOUTES les tables  
**⚠️ DANGER :** Irréversible ! Utiliser avec précaution !

---

### 25. Lancer les tests
```bash
python manage.py test
```
**Rôle :** Exécute tous les tests unitaires du projet  
**Options :**
- `python manage.py test gestion` : Tests d'une app spécifique
- `python manage.py test gestion.tests.TestProducteur` : Test d'une classe spécifique

---

## 🗂️ COMMANDES SYSTÈME (NAVIGATION)

### 26. Créer un dossier
```bash
mkdir nom_dossier
```
**Exemple :**
```bash
mkdir AgriTech-Benin
```
**Rôle :** Crée un nouveau dossier

---

### 27. Se déplacer dans un dossier
```bash
cd nom_dossier
```
**Exemple :**
```bash
cd AgriTech-Benin
```
**Rôle :** Change le répertoire courant

---

### 28. Revenir au dossier parent
```bash
cd ..
```
**Rôle :** Remonte d'un niveau dans l'arborescence

---

### 29. Afficher le contenu du dossier

**Windows :**
```bash
dir
```

**Mac/Linux :**
```bash
ls
```
**Rôle :** Liste les fichiers et dossiers du répertoire courant

---

### 30. Afficher le chemin actuel

**Windows :**
```bash
cd
```

**Mac/Linux :**
```bash
pwd
```
**Rôle :** Affiche le chemin complet du répertoire actuel

---

## 📝 COMMANDES GIT (CONTRÔLE DE VERSION)

### 31. Initialiser un dépôt Git
```bash
git init
```
**Rôle :** Crée un nouveau dépôt Git dans le dossier actuel

---

### 32. Ajouter des fichiers au staging
```bash
git add .
```
**Rôle :** Prépare tous les fichiers modifiés pour le commit  
**Options :**
- `git add fichier.py` : Ajouter un fichier spécifique
- `git add *.py` : Ajouter tous les fichiers Python

---

### 33. Créer un commit
```bash
git commit -m "Message descriptif"
```
**Exemple :**
```bash
git commit -m "Ajout des modèles de base"
```
**Rôle :** Enregistre les modifications dans l'historique Git

---

### 34. Voir l'état des fichiers
```bash
git status
```
**Rôle :** Affiche les fichiers modifiés, ajoutés, ou non suivis

---

### 35. Voir l'historique des commits
```bash
git log
```
**Rôle :** Affiche l'historique de tous les commits  
**Option utile :** `git log --oneline` (version compacte)

---

## 🎯 RÉSUMÉ DES COMMANDES LES PLUS UTILISÉES

| Commande | Fréquence | Utilisation |
|----------|-----------|-------------|
| `python manage.py runserver` | ⭐⭐⭐⭐⭐ | Chaque session de développement |
| `python manage.py makemigrations` | ⭐⭐⭐⭐ | Après chaque modification de models.py |
| `python manage.py migrate` | ⭐⭐⭐⭐ | Après makemigrations |
| `python manage.py createsuperuser` | ⭐⭐ | Une fois par projet |
| `python manage.py shell` | ⭐⭐⭐ | Pour tester/déboguer |
| `pip install package` | ⭐⭐⭐ | Quand on ajoute des dépendances |

---

## 💡 BONNES PRATIQUES

1. **Toujours activer le venv** avant de travailler
2. **Faire un commit Git** après chaque fonctionnalité terminée
3. **Tester avec runserver** après chaque modification importante
4. **Créer des migrations** dès qu'on modifie models.py
5. **Utiliser le shell** pour tester des requêtes complexes avant de les coder

---

*Document de référence - Projet AgriTech-Bénin*  
*Dernière mise à jour : 22 Janvier 2026*