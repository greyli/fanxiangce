# -*- coding: utf-8 -*-
__author__ = 'lihui'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views