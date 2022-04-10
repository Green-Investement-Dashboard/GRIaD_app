# -*- coding: utf-8 -*-
"""
© GRID Team, 2021
"""

import pandas
import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json
from agri_data import data_import

class Scoring:
    """Cette classe donne les données nécessaires au rendu des gauges indiquant les scores ESG 
    """
    def __init__ (self):
      #self.data = data_import.ReadData('scoring').read_json()
      self.data =  data_import.ReadData('graph_data').read_json()
      self.value_rg = data_import.ReadData('value_range').read_json()
    
    def main (self):
      """
        :return: liste de listes (une par indicateur) contenant pour chaque: sa valeur, la valeur max de l'echelle, une liste avec les intervalles de couleurs
        :rtype: list
        """
      list_output = []
      for indic in 'ESG':
        indic_val = self.data.loc[f'{indic}0', 'list_y'][-1]
        bin_val = self.value_rg.loc[f'{indic}0', 'Bin']
        list_output.append([indic_val, bin_val])
    
      return list_output

class CriticalAlert:
    """Cette classe donne las liste des indicateurs considérés comme critique.
    """
    def __init__(self):
      #self.data = pandas.read_csv('https://raw.githubusercontent.com/Green-Investement-Dashboard/data/main/data_eg/liste_indic.csv')
      self.data = pandas.DataFrame(columns=['Critique'])
      self.data = self.data.set_index('Code input')
    
    def main(self):
      """
        :return: liste de listes (une par indicateur) contenant pour chaque la liste des indicateurs critiques
        :rtype: list
        """
      list_env = []
      list_soc = []
      list_gouv = []
    
      for an_id in self.data[self.data['Critique']==1].index:
        if 'E' in an_id:
          list_env.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
        if 'S' in an_id:
          list_soc.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
        if 'G' in an_id:
          list_gouv.append(self.data.loc[an_id, 'Phénomène dangereux'])
    
      return [list_env, list_soc, list_gouv]



  