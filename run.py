# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us


Ce fichier est celui qui génère les pages HTML à partir des fonctions ci dessous
"""

from flask_migrate import Migrate
from flask import jsonify, render_template, redirect, request, url_for, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect

from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

import plotly
import plotly.graph_objs as go

import pandas
import numpy
import json

#Ci dessous, import des modules internes pour générer les graphs
from app.home.content_gen import index_renderer
from app.home.content_gen import map_generation as mgen
from app.home.content_gen import graph_generation as ggen
#from app.home.content_gen import questionaire

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 

Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )


@app.route('/env')
def env():
	"""Cette fonction génère la page environnement avec ses représentations graphiques

	:return: renderer de la page avec ses variables associées
    """
	plot_canicule = ggen.CaniculePlot().main()
	plot_fire = mgen.FirePlot().main()
	
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('environnement.html', canicule_map=plot_canicule, plot_fire = plot_fire, critical_alert = critical_alert)

@app.route('/gouv')
def gouv():
	"""Cette fonction génère la page gouvernance avec ses représentations graphiques

	:return: renderer de la page avec ses variables associées
    """
	critical_alert = index_renderer.CriticalAlert().main()
	G6_indic = ggen.PieChart('G6', "Diversification d'activité").main()
	G9_indic = ggen.BulletChart('G9', "Matériel mutualisé").main()

	return render_template('gouvernance.html', G6_indic=G6_indic, G9_indic=G9_indic, critical_alert = critical_alert)

@app.route('/soc')
def soc():
	"""Cette fonction génère la page social avec ses représentations graphiques

	:return: renderer de la page avec ses variables associées
    """
	S1_indic = ggen.BulletChart('S1', "Communication").main()
	S2_indic = ggen.BulletChart('S2', "Barrières douanières").main()
	S3_indic = ggen.PieChart('S3', "Diversification d'activité").main() 
	critical_alert = index_renderer.CriticalAlert().main()

	return render_template('social.html', bullet_charts = [S1_indic, S2_indic], S3_indic = S3_indic,
		critical_alert = critical_alert)

@app.route('/finance')
def finance():
	"""Cette fonction génère la page finance avec ses représentations graphiques

	:return: renderer de la page avec ses variables associées
    """
	list_graph = ggen.FinancialChart('plot_bar', 'F1', 'F2').main()

	return render_template('finance.html', ebitda=list_graph[0], endet=list_graph[1])

	

@app.route('/liste')
def index():
	"""Cette fonction génère la page index avec ses représentations graphiques

	:return: renderer de la page avec ses variables associées
    """
	sql2 =f"select * from invite"
	result2 = db.engine.execute(sql2)
	rows2 = [row for row in result2]
	print(rows2)
	df = pandas.DataFrame(data=rows2, columns=['Index', 'Email', 'Nom', 'Prenom', 'Plus 1?', 'Email +1', 'Nom +1', 'Prenom +1', 'Regime', 'Regime +1'])
	df = df[['Email', 'Nom', 'Prenom', 'Regime', 'Plus 1?', 'Email +1', 'Nom +1', 'Prenom +1', 'Regime +1']]
	df = df.replace('', numpy.nan)
	print(df)

	df1 = df[['Email', 'Nom', 'Prenom', 'Regime', 'Email +1']].reset_index(drop=True)
	df2 = df[['Email +1', 'Nom +1', 'Prenom +1', 'Regime +1', 'Email']].reset_index(drop=True)
	df2 = df2.rename(columns={'Email +1':'Email', 'Nom +1':'Nom', 'Prenom +1':'Prenom', 'Email +1':'Email', 'Regime +1':'Regime', 'Email':'Email +1'})
	df2 = df2.dropna(subset=['Email'])
	print(df1)
	print(df2)
	df_concat = pandas.concat([df1, df2], ignore_index=True)
	print(df_concat)

	return render_template('index.html', tables=[df.to_html(classes=['data', 'table'], index=False)], titles=df.columns.values,
		tables_2=[df_concat.to_html(classes=['data', 'table'], index=False)], titles_2=df_concat.columns.values,
		)

@app.route('/questionnaire', methods=['GET', 'POST'])
def set_up_q():
	"""Cette fonction génère le questionaire

	:return: renderer de la page avec ses variables associées
    """
	form = questionaire.QuestionairesAgri(request.form)

	if form.validate_on_submit():
		print('val')
		data = request.form
		result = questionaire.save_data(data)
		return render_template('questionaire.html',  end=True, message= 'Merci {}, données enregistrées'.format(form.name_exploit.data), table = result)	

	return render_template('questionaire.html',  end=False, form=form)

if __name__ == "__main__":
	app.run()
