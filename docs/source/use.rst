.. _instal:

===========================
Déploiement et installation
===========================



Déploiement en ligne
===========================

Le code est stocké sur GitHub puis déployé sur Heroku pour qu'il soit accessible en ligne. Ce choix a été fait pour simplifier la création et la visualtions du PoC dans un premier temps. Cependant, à terme, l'application sera hébergée sur Google Cloud.

La principale conséquence de ce choix est le temps que met l'application à charger.



Installation en local
===========================

Si vous le souhaitez, il est possible de faire tourner l'application en local, cependant cela nécessite Python 3.x et un manager de module type pip ou anaconda.
Pour la suite, nous supposerons que ces pré-requis sont remplis.

Pour utiliser l'application en local:

#. Clonez la branche principale du `répértoire GitHub <https://github.com/Green-Investement-Dashboard/GRID_app>`__
#. Créez un environnement virtuel soit avec :
	#. pip : :code:`python3 -m pip install -r requirements.txt`
	#. anaconda :code:`conda env create -f environment.yml`