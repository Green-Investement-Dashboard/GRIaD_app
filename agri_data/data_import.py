"""
© GRID Team, 2021
"""

import pandas 
import os

class ReadData:
	"""Cette classe lit les données json disponibles en locals et retourne une dataframe
    """
	def __init__ (self, name):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
		self.name = name


	def read_json(self):
		full_path = os.path.normcase(f'{self.current}/{self.name}.json')
		df = pandas.read_json(full_path, orient='table')

		return df

