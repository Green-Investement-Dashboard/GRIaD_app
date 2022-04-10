"""
© GRID Team, 2021
"""

import pandas
import numpy
import os
from app import SAVE_MODE, DEMO_MODE

class RandomDraw:
	"""Cette classe télécharge les données de GitHub et les stocke en local. Pour certains jeux de données, ils sont modifiés par un tri 
	alétoire à chaque login
    """

	def __init__(self):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
		self.root_link = 'https://raw.githubusercontent.com/Green-Investement-Dashboard/data/data_v2/data_eg'

	def data_agri (self):
		"""Télécharge et enregistre les données liées à l'emplacement de l'agriculteur.
        """
		df_data_agri = pandas.read_json(f'{self.root_link}/data_agri.json', orient='table')

		full_path = os.path.normcase(f'{self.current}/data_agri.json')
		df_data_agri.to_json(full_path, orient='table', indent=4)
		print('Saved Data Agri')

	def graph_val (self):
		"""Télécharge et enregistre les données pour générer les graphs.
        """
		self.df_graph_val = pandas.read_json(f'{self.root_link}/graph_val.json', orient='table')
		self.financial_draw()
		self.scoring_draw()
		print(self.df_graph_val)

		full_path = os.path.normcase(f'{self.current}/graph_data.json')
		self.df_graph_val.to_json(full_path, orient='table', indent=4)
		print('Saved Graph Val')

	def indic_critique (self):
		"""Télécharge et enregistre les données donnant les indices critiques.
        """
		df_indic_critique = pandas.read_csv(f'{self.root_link}/liste_indic.csv')

		full_path = os.path.normcase(f'{self.current}/indic_data.json')
		df_indic_critique.to_json(full_path, orient='table', indent=4)
		print('Saved Index Critique')

	def value_rg (self):
		"""Télécharge et enregistre les données donnant l'amplitude de valeurs des données
        """
		df_v_range = pandas.read_json(f'{self.root_link}/value_range.json', orient='table')
		
		full_path = os.path.normcase(f'{self.current}/value_range.json')
		df_v_range.to_json(full_path, orient='table', indent=4)
		print('Saved Value range')


	def financial_draw (self):
		"""Randomisation des données financières en 2 étapes:
		1- Selection d'une valeur initiale alétoire dans un intervalle
		2- Tirage aléatoire par rapport à la valeur précédente dans un intervalle
		"""
		v0 = {'F1':1000, 'F2':1.2} #Valeurs initials
		var = {'F1': [0.9, 1.1], 'F2': [0.90, 1.1]} #Range de l'interval en %

		for index in v0.keys() :
			new_list = [round(numpy.random.random()*(var[index][1]*v0[index] - var[index][0]*v0[index]) + var[index][1]*v0[index],2)]
			for k in range(len(self.df_graph_val.loc[index, 'list_x'])-1):
				rd_num = numpy.random.random()*(var[index][1]*new_list[-1] - var[index][0]*new_list[-1]) + var[index][1]*new_list[-1]
				new_list.append(round(rd_num,2))

			self.df_graph_val.loc[index,'list_y'] = new_list

	def scoring_draw (self):
		"""Randomisation des données de scoring dans un intervalle donné
		"""
		intervalles = {'E0':[43,72], 'S0':[45,55], 'G0':[55,100]}
		
		for index in intervalles.keys():
			self.df_graph_val.loc[index, 'list_y'] = [numpy.random.randint(intervalles[index][0], intervalles[index][1])]

	

	def main(self):
		if DEMO_MODE:
			print('Demo mode')
		else:
			self.data_agri()
			self.graph_val()
			self.indic_critique()
			self.value_rg()
			print('data_generated')
