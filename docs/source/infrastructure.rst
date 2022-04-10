================
Infrastructure
================

Organisation globale du répertoire
==================================

Le répertoire est organisé autour de deux principaux modules :

* :code:`app` : module générant l'application et ses rendus
* :code:`agri_data` : module regroupant et générant les données

Le fichier principal qui lance l'application est situé à la racine, il s'appelle :code:`run.py`

.. code-block:: bash

   |
   |-- app/                                      # L'application en elle même
   |    |-- home/                                # Génération des contenus spécifiques pas page HTML spécifiques
   |    |-- base/                                # Blueprint, contient la structure de l'application
   |
   |-- agri_data/                                # Génération des données
   |
   |-- ************************************************************************


Point de vue Flask App / Python
==================================

Le module :code:`app` est organisé en 2 sous-modules :

* :code:`home` qui sert à générer les visuels, en particulier le sous-module :code:`content_gen`
* :code:`base` qui sert à gérer l'authentification

Le code est ensuite commenté et précisé dans les modules :ref:`agri` et :ref:`app`

La structure du répértoire ,d'un point de vue Python, est la suivante:

.. code-block:: bash

   |
   |-- app/                                      # L'application en elle même
   |    |-- home/                                
   |         |-- content_gen/                    # Module générant les visuels
   |         |    |-- data/                      # Données externes pré-traitées  
   |         |    |-- graph_generation.py        # Génération des graphiques
   |         |    |-- index_renderer.py          # Génération de l'index
   |         |    |-- map_generation.py          # Génération des cartes
   |         |    |-- questionaire.py.py         # Génération du questionnaire agri
   |         |-- routes.py
   |  
   |    |-- base/                                
   |         |-- forms.py                        # Script gérant le formulaire de login et d'inscription
   |         |-- models.py                       # Script gérant la lecture de la base de données des logins
   |         |-- routes.py                       # Script gérant les actions 
   |         |-- util.py                         # Script gérant le hachage du mot de passe
   |
   |-- agri_data/                               
   |    |-- data_draw.py                         # Tirage aléatoire des données 
   |    |-- data_import.py                       # Import des données de GitHub
   |    |-- *.json
   |
   |-- requirements.txt                          # Librairies nécessaires pour faire fonctionner le code
   |-- environment.yml                           # Environnement anaconda
   |-- requirements-mysql.txt                    # Module nécessaire pour Mysql DMBS
   |-- requirements-pqsql.txt                    # Module nécessaire pour PostgreSql DMBS
   |
   |-- .env                                      # Variable environnement 
   |-- config.py                                 # Configuration de l'application
   |-- run.py                                    # Lancement de l'application
   |
   |-- ************************************************************************



Point de vue fronte-end / HTML
==================================

Les fichiers HTML sont organisés autour de 2 dossiers:

* **/home** : ici sont stockés les fichiers HTML des pages du dashboard
* **/base** : ici sont stockés les fichiers HTML servant de modèles pour générer les pages


.. code-block:: bash

   |
   |-- app/
   |    |-- home/
   |         |-- templates/                       # Ensemble des pages HTML
   |         |    |    |-- *.html
   |  
   |    |-- base/                                
   |         |-- static/
   |         |    |-- <css, JS, images>          # Fichiers CSS, Javascripts et images
   |         |
   |         |-- templates/                      # Modèles pour le rendu des pages
   |              |
   |              |-- includes/                  
   |              |    |-- navigation.html       # Menu du haut
   |              |    |-- sidebar.html          # Menu latéral
   |              |    |-- footer.html           # Pied de page
   |              |    |-- scripts.html          # Scripts communs aux pages HTML
   |              |
   |              |-- layouts/                   # Pages masters
   |              |    |-- base.html             # Layout des pages
   |              |
   |              |-- accounts/                  # Pages authentification
   |                   |-- login.html            # Page de Login
   |                   |-- register.html         # Page d'inscription
   |
   |-- ************************************************************************


