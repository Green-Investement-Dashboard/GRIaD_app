# -*- coding: utf-8 -*-
"""
© GRID Team, 2021
"""


import plotly.graph_objects as go
import pandas
import os
import networkx as nx
import matplotlib.pyplot as plt

class BuildingNetwork:
	"""Cette classe sert ? générer un objet NetworkX pour ploter"""

	def __init__(self):
		self.current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
		self.G = nx.Graph()

	def nodes (self):
		vertices = [('Agriculteur', {'type':'Agri'}), 
		('Distributeur 1', {'type':'Distributeur'}), ('Distributeur 2', {'type':'Distributeur'}), ('Distributeur 3', {'type':'Distributeur'}),
		('Phyto sanitaire 1', {'type':'Fournisseur'}), ('Phyto sanitaire 2', {'type':'Fournisseur'}), ('Phyto sanitaire 3', {'type':'Fournisseur'})
		]

		self.G.add_nodes_from(vertices)

	def edges (self):
		edge = [('Agriculteur', 'Distributeur 1'), ('Agriculteur', 'Phyto sanitaire 1')]

		self.G.add_edges_from(edge)

	def plot (self):
		pass


	def main(self):
		self.nodes()
		self.edges()
		self.plot_test()
		print(list(self.G.nodes))

if __name__ == '__main__':
	BuildingNetwork().main()