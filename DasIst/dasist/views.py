# -*- coding: UTF-8 -*-
__author__ = 'sdv'

from dasist import app
from flask import render_template, flash, redirect, session, url_for, request, g

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
def index():
    """Just a generic index page to show."""
    return render_template('index.html')
