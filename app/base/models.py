# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Sert à lire et écrire dans la db des logins
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Boolean

from app import db, login_manager
from app import db, login_manager

from app.base.util import hash_pass
"""
class Invite(db.Model, UserMixin):

    __tablename__ = 'invite'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    nom = Column(String)
    prenom = Column(String)
    plus1 = Column(Boolean)
    email_plus1 = Column(String, unique=True)
    nom_plus1 = Column(String)
    prenom_plus1 = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)


    def __repr__(self):
        return str(self.email)
"""
class User(db.Model, UserMixin):

    __tablename__ = 'invite'

    id = Column(Integer, primary_key=True)
    #username = Column(String, unique=True)
    email = Column(String, unique=True)
    nom = Column(String)
    prenom = Column(String)
    regime = Column(String)
    plus1 = Column(String)
    email_plus1 = Column(String, unique=True)
    nom_plus1 = Column(String)
    prenom_plus1 = Column(String)
    regime_plus1 = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)


    def __repr__(self):
        return str(self.email)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None
