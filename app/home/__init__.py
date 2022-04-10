# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)
