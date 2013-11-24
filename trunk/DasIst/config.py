# -*- coding: UTF-8 -*-
__author__ = 'ti.eugene@gmail.com'

import os
_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED=True
DEBUG_TB_INTERCEPT_REDIRECTS=False


ADMINS = frozenset(['ti.eugene@gmail.com'])
SECRET_KEY = 'N07Vu9No4DVRyt9IDZkw5VTyD'


# ========================= Database section =========================
DB_FILE = os.path.join(_basedir, 'adolat.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'dasist.db')
DATABASE_CONNECT_OPTIONS = {'convert_unicode':'True'}
SQLALCHEMY_ECHO=True
#SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
# ========================= End of DB Section =========================

THREADS_PER_PAGE = 100

# WTF_CSRF_ENABLED = False
# WTF_CSRF_SESSION_KEY = "PP2uY64X3aLB224CUmKx9cVY6QnIiMtuc7y1HesI4GKcv85TEED"
CSRF_ENABLED = False
CSRF_SESSION_KEY = "PP2uY64X3aLB224CUmKx9cVY6QnIiMtuc7y1HesI4GKcv85TEED"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LfiuOgSAAAAAEqWmJWz9b3m7wiRse2s8RJMQEHa'
RECAPTCHA_PRIVATE_KEY = '6LfiuOgSAAAAAMmtOuvtDT4cB9JbKke9x6sLbqJ3'
RECAPTCHA_OPTIONS = {'theme': 'white', 'lang' : 'ru'}

SESSION_COOKIE_SECURE = True

#SERVER_NAME = '127.0.0.1:5000'
