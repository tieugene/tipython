# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

# Импорт зависимостей
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
#from flask_wtf.csrf import CsrfProtect


#CsrfProtect(app)
db = SQLAlchemy(app)

# the toolbar is only enabled in debug mode:
# adolat.debug = True
toolbar = DebugToolbarExtension(app)

#from adolat.users.views import mod as usersModule
#adolat.register_blueprint(usersModule)

from dasist.blueprints.contacts.views import contacts as contactsModule
app.register_blueprint(contactsModule)

import views, models
