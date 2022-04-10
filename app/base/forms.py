# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Génère les formulaires d'inscription et de connexion
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, IntegerField, RadioField, HiddenField
from wtforms.validators import InputRequired, Email, DataRequired, Length

class LoginForm(FlaskForm):
    email = TextField    ('Email'        , id='email_create'    , validators=[DataRequired(), Email()])

class CreateAccountForm(FlaskForm):
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    prenom = TextField('Prenom')
    nom = TextField('Nom')
    plus1 = RadioField(choices=[("Non",'Non'),("Oui", 'Oui')])
    email_plus1    = TextField('Email'        , id='email_create'    , validators=[Email()])
    prenom_plus1 = TextField('Prenom plus 1')
    nom_plus1 = TextField('Nom plus 1')

class EditAccountForm(FlaskForm):
    email    = HiddenField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    prenom = TextField('Prenom')
    nom = TextField('Nom')
    plus1 = RadioField(choices=[("Non",'Non'),("Oui", 'Oui')])
    email_plus1    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    prenom_plus1 = TextField('Prenom plus 1')
    nom_plus1 = TextField('Nom plus 1')



