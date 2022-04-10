===========================
Introduction
===========================



Se connecter
===========================

Pour voir le dashboard, rendez-vous sur `app.grid-tech.fr <http://app.grid-tech.fr>`__ .

Pour les besoins de la démonstration dans le cadre du concours FIFG, un compte test a été créé :

* **Nom d'utilisateur**: test
* **Mot de passe**: test

.. tip::
   Avec notre infrastructure actuelle, le chargement des pages peut paraître long mais nous travaillons pour y remédier.

.. attention::
   Le dashboard est pour le moment optimisé pour les écrans d'ordinateurs.

Pour plus de détails sur le déploiement :ref:`instal`


Les données
============


Les données d'entrée
---------------------

Le GRID fonctionne à partir de 2 types de données d'entrée:

* Les données externes provenant de Météo France, Copernicus, etc ;
* Les données liées à l'exploitation :
	* Données internes rentrées par l'agriculteur dans un questionnaire ;
	* Données financières provenant de l'établissement bancaire. 


Données pour le PoC
---------------------

Pour le PoC, afin de démontrer la capacité dynamique du dashboard, à chaque login, une partie des données sont tirées au hasard, en particulier celles relatives :

* aux scores RSE présentés sur la première page
* aux données financières (cf page indicateur et le module `agri_data` pour plus de détail)

Toutes les données sont disponibles `ici <https://github.com/Green-Investement-Dashboard/data/tree/main/data_eg>`__

Pour plus de détail sur les données et leur exploitation :ref:`indic`


Le code
==========
Vous pouvez retrouver notre code dans son intégralité `ici <https://github.com/Green-Investement-Dashboard/GRID_app>`__.



