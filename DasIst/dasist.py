#!/bin/env python
# -*- coding: utf-8 -*-
# Description:
__author__ = 'ti.eugene@gmail.com'

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

from blueprints.contacts.views import contacts as contactsModule
app.register_blueprint(contactsModule)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    """Just a generic index page to show."""
    return render_template('index.html')

# 1. standalone
if __name__ == '__main__':
	application = web.application(('/', 'index'), globals())
	application.internalerror = web.debugerror
	application.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(('/', 'index'), globals()).wsgifunc()
