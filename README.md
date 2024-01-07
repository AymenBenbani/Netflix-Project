# Guide d'Installation de Django [ Windows ]

Ce guide vous aidera à installer Django, un framework web populaire pour le développement en Python, sur votre système Windows.

## Prérequis

- Python (version 3.6 ou supérieure recommandée)
  - Téléchargez et installez Python depuis [le site officiel](https://www.python.org/downloads/).
  - Assurez-vous d'ajouter Python à la variable d'environnement PATH lors de l'installation.

## Installation de Django

1. **Ouvrez une invite de commandes ou PowerShell en tant qu'administrateur :**
   - Cliquez avec le bouton droit sur le menu Démarrer.
   - Sélectionnez "Invite de commandes (admin)" ou "PowerShell (admin)".

2. **Installez Django en utilisant pip :**
   ```bash
   pip install django

## Vérifiez l'installation :
  python -m django --version

## Création d'un Projet Django :
1.Créez un nouveau répertoire pour votre projet :
  mkdir MonProjetDjango
  cd MonProjetDjango
2.Initialisez votre projet Django :
  django-admin startproject nom_du_projetdjango-admin startproject nom_du_projet
3.Accédez au répertoire du projet :
  cd nom_du_projet
## Exécution du Serveur de Développement :
1.Appliquez les migrations initiales :
  python manage.py migrate
2.Lancez le serveur de développement :
  python manage.py runserver
Le serveur sera accessible à l'adresse http://127.0.0.1:8000/.
3.Accédez à l'application Admin (facultatif) :
  Visitez http://127.0.0.1:8000/admin/ dans votre navigateur.
  Utilisez les informations d'identification de l'administrateur créées lors des migrations.

## Lancer notre projet :
1. Mettre les fichiers et les dossiers du Repository dans un dossier
2. Ouvrir un terminal et se placer sur ce dossier
3. Taper sur la ligne de commande : .\env\Scripts\activate
4. Taper sur la ligne de commande : pip install -r requirements.txt
5. Taper sur la ligne de commande : python manage.py runserver
6. Acceder à l'adresse http://127.0.0.1:8000/ .

