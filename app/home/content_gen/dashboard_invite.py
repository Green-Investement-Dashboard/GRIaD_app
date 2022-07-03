"""
Clément Houzard 
July, 2
"""

import pandas
import plotly.graph_objects as go
import json
import plotly
import numpy
from plotly.subplots import make_subplots

class DataPreparation:
	URL = 'https://docs.google.com/spreadsheets/d/1aFWy3aq3cwQYYTzDHDft_PqAC94e4Kw3LXzB6B5S3Ug/export?format=csv&gid=52273500'
	def __init__(self):
		pass

	def read_data(self):
		self.df_full = pandas.read_csv(self.URL)
		self.df_full.columns = ['Horodateur', 'Adresse e-mail', 'Serez-vous present', 'Prénom', 'Nom',
       'Régime', 'Plus 1', 'Prénom.1', 'Nom.1', 'E-mail',
       'Régime.1', 'Montant attendu', 'Montant regle', 'Train arrivée',
       "Heure d'arrivée", 'Train départ', 'Heure départ']

	def prepare_data(self):
		main_guest = self.df_full[['Horodateur', 'Adresse e-mail', 'Serez-vous present',	'Prénom', 'Nom', 'Régime', 
                      'Plus 1', 'E-mail', 'Montant attendu', 'Montant regle', 'Train arrivée', "Heure d'arrivée", 'Train départ', 'Heure départ']]
		main_guest['Statut'] = 'Main'
		main_guest = main_guest.rename(columns={'Adresse e-mail':'Main email', 'Serez-vous present':'Main RSVP', 
		                                                  'Plus 1':'Secondary RSVP', 'E-mail':'Secondary email'})
		main_guest = main_guest.dropna(subset=['Horodateur'])

		secondary_guest = self.df_full[['Horodateur', 'E-mail', 'Plus 1', 'Prénom.1', 'Nom.1', 'Régime.1', 
                                'Serez-vous present', 'Adresse e-mail', 'Montant attendu', 'Montant regle', 'Train arrivée',	"Heure d'arrivée",	'Train départ', 'Heure départ']]
		secondary_guest['Statut'] = 'Secondary'
		secondary_guest = secondary_guest.rename(columns={'E-mail':'Main email', 'Plus 1':'Main RSVP',	'Prénom.1':'Prénom', 'Nom.1':'Nom', 'Régime.1':'Régime', 
		                                                  'Serez-vous present':'Secondary RSVP', 'Adresse e-mail':'Secondary email'})
		secondary_guest = secondary_guest.dropna(subset=['Main email'])
		
		self.guests = main_guest.merge(secondary_guest, how='outer')
		self.guests = self.guests.replace({'Main RSVP':{'Oui, je serai là.':True, 'Désolé, je ne peux pas venir.':False, 'Oui': True, 'Non':False},
		                        'Secondary RSVP':{'Oui, je serai là.':True, 'Désolé, je ne peux pas venir.':False, 'Oui': True, 'Non':False}})
		self.guests['Montant attendu'] = self.guests.loc[:,'Montant attendu'].apply(lambda x: x[:-1])
		self.guests['Montant regle'] = self.guests.loc[:,'Montant regle'].apply(lambda x: x[:-1])
		self.guests[['Montant attendu', 'Montant regle']] = self.guests[['Montant attendu', 'Montant regle']].apply(pandas.to_numeric)
		self.guests.loc[self.guests['Montant attendu']>60, ['Montant attendu', 'Montant regle']] = self.guests[['Montant attendu', 'Montant regle']]/2
		self.guests['Horodateur'] = pandas.to_datetime(self.guests['Horodateur'], format='%d/%m/%Y %H:%M:%S')
		print(self.guests.columns)

	def kpi (self):
		self.nb_ppl = self.guests.loc[self.guests['Main RSVP']].shape[0]
		self.nb_main_ppl = self.guests.loc[(self.guests['Main RSVP']) & (self.guests['Statut']=='Main')].shape[0]
		self.nb_sec_ppl = self.guests.loc[(self.guests['Main RSVP']) & (self.guests['Statut']=='Secondary')].shape[0]
		self.money_theo = self.guests['Montant attendu'].sum()
		self.money_actual = self.guests['Montant regle'].sum()
		self.vege = self.guests.loc[(self.guests['Main RSVP']) & (self.guests['Régime']=='Végétarien')].shape[0]

	def sign_up (self):
		self.evol_signup = self.guests[['Horodateur', 'Main RSVP']]
		self.evol_signup = self.evol_signup.replace({True:1, False:0})
		self.evol_signup = self.evol_signup.groupby('Horodateur').sum()
		self.evol_signup = self.evol_signup.sort_index()
		self.evol_signup = self.evol_signup.cumsum()
		print(self.evol_signup)
		#self.evol_signup.index = pandas.to_datetime(self.evol_signup.index)

	def signup_indic (self):
		data = go.Figure(go.Indicator(mode = "number+gauge",
			gauge = {
			#'shape': "bullet", 
			'axis': {'range': [None, 46]}},
			value = self.nb_ppl,
			domain = {'x': [0 ,1], 'y': [0, 1]},
			title = {'text': "Nombre de personnes inscrites"}))
		layout = go.Layout(height=100, 
                   paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                         )
		fig = go.Figure(data, layout)
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return plot_json

	def signup_type_indic (self):
		df_signup = self.guests.loc[(self.guests['Main RSVP']), ['Statut', 'Main RSVP']].groupby('Statut').count()
		df_signup = df_signup.rename(index={'Main':'Invités principaux', 'Secondary':'Plus 1'})

		self.color = ['#72B857', '#3D3D34']
		data = [go.Bar(name=df_signup.index[k],  x=['Invités'], y=[df_signup['Main RSVP'][k]], marker_color=self.color[k]) for k in range(len(df_signup.index))]
		layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title="", font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0),
                         barmode='stack',
                         )

		fig = go.Figure(data, layout)
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return plot_json

	def vege_indic (self):
		df_vege = self.guests.loc[(self.guests['Main RSVP']), ['Régime', 'Main RSVP']].groupby('Régime').count()

		data = [go.Bar(name=df_vege.index[k],  x=['Invités'], y=[df_vege['Main RSVP'][k]], marker_color=self.color[k]) for k in range(len(df_vege.index))]
		layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title="", font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0),
                         barmode='stack',
                         )

		fig = go.Figure(data, layout)
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return plot_json

	def evol_signup_indic (self):
		data = go.Scatter(x=self.evol_signup.index, y=self.evol_signup['Main RSVP'])
		print(self.evol_signup.index)
		layout = go.Layout(paper_bgcolor='rgba(61,61,51,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis_title='Date' , yaxis_title="Nombre d'inscrits", font=dict(color='#5cba47'), margin=dict(l=0, r=20, t=20, b=0),
                         )
		fig = go.Figure(data, layout)
		
		fig.add_shape(type='line',
                x0=self.evol_signup.index[0],
                y0=46,
                x1=pandas.to_datetime("2022-10-08", format="%Y-%m-%d"),
                y1=46,
                line=dict(color='#72B857'),
                xref='x',
                yref='y')
        
		#fig.add_hline(y=40, line_width=3, line_dash="dash", line_color="green")

		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return plot_json

	def finance_indic (self):
		data = go.Figure(go.Indicator(mode = "number+gauge",
			gauge = {
			#'shape': "bullet", 
			'axis': {'range': [None, 46*60], 'ticksuffix':'€'},
			'steps': [{'range': [0, self.money_theo], 'color': "lightgray"},]
                 },
			value = self.money_actual,
			number = {'suffix':"€"},
			domain = {'x': [0 ,1], 'y': [0, 1]},
			title = {'text': "Argent reçu"},))
		layout = go.Layout(height=100, 
                   paper_bgcolor='rgba(61,61,51,0.01)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#5cba47'),
                         )
		fig = go.Figure(data, layout)
		plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
		return plot_json

	def list_invite (self):
		self.df_show = self.df_full.dropna(subset=['Horodateur'])
		self.df_show.columns = ['Horodateur', 'Adresse e-mail principal', 'Serez-vous present?', 'Prénom', 'Nom',
	       'Régime', 'Plus 1?', 'Prénom +1', 'Nom +1', 'E-mail +1',
	       'Régime +1', 'Montant attendu', 'Montant regle', 'Train arrivée',
	       "Heure d'arrivée", 'Train départ', 'Heure départ']

		self.tables_show=[self.df_show.to_html(classes=['data', 'table'], index=False)]
		self.titles_show=self.df_show.columns.values

		self.df_show_table = self.guests
		self.tables_show_united=[self.df_show_table.to_html(classes=['data', 'table'], index=False)]
		self.titles_show_united=self.df_show_table.columns.values

	def main (self):
		self.read_data()
		self.prepare_data()
		self.kpi()
		self.sign_up()

