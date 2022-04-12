# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Gère les routines des connnexions et inscription
"""

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
import pandas, os
import pyotp

from app import db, login_manager

from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, EditAccountForm
from app.base.models import User

from app.base.util import verify_pass

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

import run
from agri_data import data_draw

import qrcode

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # read form data
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        print(user)
        print('C2', request.form)

        if user:
            login_user(user)
            #data_draw.RandomDraw().main()

            #render = run.index()
            #return render
            return redirect(f"/modify2")
                
        else:
            return redirect(f"/register")

        """
            login_user(user)
            data_draw.RandomDraw().main()

            render = run.index()
            return render
        """
        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Utilisateur non existant ou mot de passe incorrecte', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form, user='test')

    #render = run.index()
    #return render
    return redirect(f"/modify2")


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        if 'cle' not in request.form.keys():
            email  = request.form['email']

            # Check usename exists
            user = User.query.filter_by(email=email).first()
            
            if user:
                return render_template( 'accounts/register.html', 
                                        msg='Username already registered',
                                        success=False,
                                        register = True,
                                        registration = True,
                                        form=create_account_form)
                
            
            user = User(**request.form, 
                #**data
                )
            print(user)
            
            db.session.add(user)
            db.session.commit()
            
            return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    register = False,
                                    registration=True,
                                    form=create_account_form)
            

        else:
            return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    register = False,
                                    registration=True,
                                    form=create_account_form)

            """
            user = User.query.filter_by(username=username).first()
            key = user.two_fa_key
            current_var_key = pyotp.TOTP(key).now()

            current = os.path.normcase(os.path.dirname(os.path.realpath(__file__)))
            file_name='qrcode_test.png'
            full_path = os.path.normcase(f'{current}/static/assets/img/{file_name}')

            print (int(request.form['cle']))
            print(current_key)
            print(type(current_key))

            if request.form['cle'] == current_key:
                print('hey')
                return render_template( 'accounts/register.html', 
                                    msg='User created please <a href="/login">login</a>', 
                                    success=True,
                                    register = False,
                                    registration=True,
                                    form=create_account_form)
            else:
                return render_template( 'accounts/register.html',
                                    register = True,
                                    registration=False,
                                    form=create_account_form)
            """

    else:
        return render_template( 'accounts/register.html', form=create_account_form, register = True, registration=True)

@blueprint.route('/modify2', methods=['GET', 'POST'])
def modify():
    form = EditAccountForm(request.form)
    #create_account_form = CreateAccountForm(request.form)

    if request.method == 'POST':
        print(form.errors)

        if form.is_submitted():
            print ("submitted")
        if form.validate():
            print ("valid")

        # if form.validate_on_submit():
        #     print('OK')
        print('here1')
        email = form.email.data
        prenom = form.prenom.data
        nom = form.nom.data
        regime = form.regime.data
        plus1 = form.plus1.data
        email_plus1 = form.email_plus1.data
        prenom_plus1 = form.prenom_plus1.data
        nom_plus1 = form.nom_plus1.data
        regime_plus1 = form.regime_plus1.data

        if form.plus1.data == 'Non':
            form.plus1.data = 'Non'
            form.email_plus1.data = ''
            form.prenom_plus1.data = ''
            form.nom_plus1.data = ''
            plus1 = form.plus1.data
            email_plus1 = form.email_plus1.data
            prenom_plus1 = form.prenom_plus1.data
            nom_plus1 = form.nom_plus1.data
            regime_plus1 = form.regime_plus1.data
            sql = f"update invite set email='{email}' , prenom='{prenom}', nom='{nom}', plus1='{plus1}', email_plus1='' , prenom_plus1='', nom_plus1='', regime='{regime}', regime_plus1='' where id='{current_user.id}'"                      
            sql = f"update invite set email='{email}' , prenom='{prenom}', nom='{nom}', plus1='{plus1}', email_plus1='{email_plus1}' , prenom_plus1='{prenom_plus1}', nom_plus1='{nom_plus1}', regime='{regime}', regime_plus1='{regime_plus1}' where id='{current_user.id}'"                      
        
        else:
            sql = f"update invite set email='{email}' , prenom='{prenom}', nom='{nom}', plus1='{plus1}', email_plus1='{email_plus1}' , prenom_plus1='{prenom_plus1}', nom_plus1='{nom_plus1}', regime='{regime}', regime_plus1='{regime_plus1}' where id='{current_user.id}'"                      
        print('here')
        print(sql)
        result = db.engine.execute(sql)

        return render_template('page-user.html', title='Edit Account', form=form)


    else:
        sql =f"select * from invite where id='{current_user.id}'"
        print(sql)

        result = db.engine.execute(sql)
        rows = [row for row in result]
        if len(rows)!=0:
            for row in rows:
                form.email.data = row[1]
                form.nom.data = row[2]
                form.prenom.data = row[3]
                form.regime.data = row[8]

                form.plus1.data = row[4]

                form.email_plus1.data = row[5]
                form.nom_plus1.data = row[6]
                form.prenom_plus1.data = row[7]
                form.regime_plus1.data = row[9]
            return render_template('page-user.html', title='Edit Account', form=form)
        return redirect('/')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'





## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
