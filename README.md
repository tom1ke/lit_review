# LIT Review
Critique de livres à la demande.

Version : Python 3.10.1

## Paramétrage
- Cloner ce dépôt de code avec la commande
```$ git clone clone https://github.com/tom1ke/lit_review.git```
- Se positionner à la racine du projet via le terminal
- Créer un environnement virtuel avec la commande

> MacOS / Linux ```$ python3 -m venv env```

> Windows ```$ python -m venv env```
- Activer l'environnement virtuel avec la commande

> MacOS / Linux ```$ source env/bin/activate```

> Windows ```$ env\Scripts\activate```
- Installer les dépendances du projet avec la commande ```$ pip install -r requirements.txt```
- Se positionner au niveau de projet Django via le terminal avec la commande ```$ cd lit_review```
- Démarrer le serveur local avec la commande ```$ python manage.py runserver```
- Accéder à l'application via un navigateur à cette url : http://127.0.0.1:8000/

Cela vaut uniquement pour l'installation initiale. Pour les lancements ultérieurs, il suffira d'activer l'environnement
virtuel et de démarrer le serveur pour accéder à l'application.

## Administration
Afin d'accéder à l'interface d'administration de l'application il est nécessaire de créer un profil de *superuser*.

Pour ce faire, se positionner au niveau du projet Django via le terminal et utiliser la commande ```$ python manage.py createsuperuser```

Suivre les instructions données dans le terminal (le nom d'utilisateur et le mot de passe sont indispensables, mais il 
n'est pas nécessaire de renseigner une adresse email).

Il est maintenant possible de se connecter avec les indentifiants nouvellement créés à l'interface d'admninistration de
l'application à cette url : http://127.0.0.1:8000/admin/