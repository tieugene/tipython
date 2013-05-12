# -*- coding: utf-8 -*-
# Django settings for tidjango.sro.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('admin', 'ti.eugene@gmail.com'),
)

MANAGERS = ADMINS
DATABASE_ENGINE =	'mysql'
DATABASE_NAME =		''
DATABASE_USER =		'lansite'
DATABASE_PASSWORD =	'lansite'
DATABASE_HOST =		'localhost'
DATABASE_PORT =		''

SEND_EMAILS =		False
EMAIL_HOST =		''
EMAIL_HOST_USER =	''
EMAIL_HOST_PASSWORD =	''
EMAIL_ADDRESS_FROM =	''
if DEBUG:
	EMAIL_FAIL_SILENTLY = False
else:
	EMAIL_FAIL_SILENTLY = True

TIME_ZONE = 'Europe/Moscow'
DATE_FORMAT = 'd/m/Y'
LANGUAGE_CODE = 'ru-RU'
DEFAULT_CHARSET = 'utf-8'
SITE_ID = 1
USE_I18N = True
FILE_CHARSET = 'utf-8'
SESSION_SAVE_EVERY_REQUEST = False
SECRET_KEY = '#*9#i03#2cy2p&z9bogb0s5sq+(cay6z!5p$8!i&2=mdqddjwa'

import sys, os
PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'apps.sro2.mid.GlobalRequestMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'django.middleware.doc.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'context_processors.host',
	'context_processors.my_media_url',
	'sro2.views.my_context',
	'gw.views.gw_context',
	'views.common_context',	
)

TEMPLATE_DIRS = (
	os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.databrowse',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.databrowse',
	'django_extensions',
#	'south',
	'apps.ref',
	'apps.gw',
	'apps.sro2',
)

ADMIN_MEDIA_PREFIX =	'/admin_media/'
ADMIN_MEDIA_ROOT =	'/admin_media/'

STATIC_URL =		'/static/'
STATIC_ROOT =		os.path.join(PROJECT_DIR, 'static')

MEDIA_URL =		'/media/'

CACHE_BACKEND =		'memcached://127.0.0.1:11211/'

try:
	f=open(os.path.join(PROJECT_DIR, 'ver'),'r')
	VERSION=f.read()
	f.close()
except:
	VERSION=''

try:
	from local_settings import *
except ImportError:
	pass
