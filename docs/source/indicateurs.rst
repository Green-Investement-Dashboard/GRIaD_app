.. _indic:

===========================
Indicateurs et graphiques
===========================

Les types de représentations
=============================

Afin de rendre compte au mieux des données, nous utilisons trois types de représentations:

* **Compteurs**: ceux-ci codés en JS représentent les 3 scores ESG sur la page d'accueil.
* **Graphiques**: que ce soit des graphiques lignes ou à barres ils servent à représenter l'évolution temporelle d'un indicateur .
* **Echelles de couleurs**: lorsque qu'un indicateur est calculé à partir d'un modèle, il est représenté sous la forme d'une échelle de couleurs comme on peut le retrouver dans l'onglet Social avec le rayonnement de l'exploitation.
* **Cartes**: ce support est utilisé pour représenter des données spatiales avec une dimension temporelle.


Exemple d'indicateurs
===========================

Carte des feu de forêts
------------------------

Sur la base des données `du Climate Data Store <https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-tourism-fire-danger-indicators?tab=overview>`__, base de données de l'UE, nous avons pu exporter ces données, les traiter et les nettoyer pour notre usage. Nous avons décidé de choisir les données du modèle du GIEC RCP 4.5 car celui-ci correspond au scenario le plus probable.
Ces données ont ensuite été présentées sur une carte disponible dans l'onglet Environnement.


Graph des canicules
------------------------

Toujours sur la base des données `du Climate Data Store <https://cds.climate.copernicus.eu/cdsapp#!/dataset/sis-heat-and-cold-spells?tab=overview>`__, nous avons selectionner ces données représentant le nombre de jours de canicule. Il nous est paru plus pertinent de représenter les jours de canicule uniquement à l'emplacement du viticultuteur.