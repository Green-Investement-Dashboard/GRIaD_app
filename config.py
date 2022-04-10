# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us

Configure l'appli
"""

import os
from   decouple import config

class Config(object):
    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db_griad.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Captcha
    SSL = config('RECAPTCHA_USE_SSL', default= False)
    PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='6LePyrYaAAAAAJeb9GJ1HPDNq1izagSaVx-g_a2L')
    PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='6LePyrYaAAAAAF28HOd3ui8MsFhvF7BeUkeH7Fpc')

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='appseed'       ),
        config( 'DB_PASS'     , default='password'      ),
        config( 'DB_HOST'     , default='localhost'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='appseed-flask' )
    )

    if 'aa1f6sswky624mm.cexwsgkiousa.eu-west-3.rds.amazonaws.com' in os.environ:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config( 'DB_ENGINE'   , default='postgresql'    ),
        config( 'DB_USERNAME' , default='appseed'       ),
        config( 'DB_PASS'     , default='password'      ),
        config( 'DB_HOST'     , default='aa1f6sswky624mm.cexwsgkiousa.eu-west-3.rds.amazonaws.com'     ),
        config( 'DB_PORT'     , default=5432            ),
        config( 'DB_NAME'     , default='aa1f6sswky624mm' )
    )

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
