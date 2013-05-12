# -*- coding: utf-8 -*-
# Django settings for tidjango.lansite.

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
DATE_INPUT_FORMATS = ['%d/%m/%Y']
LANGUAGE_CODE = 'ru-RU'
DEFAULT_CHARSET = 'utf-8'
SITE_ID = 1
USE_I18N = True
FILE_CHARSET = 'utf-8'
SESSION_SAVE_EVERY_REQUEST = False
SECRET_KEY = '#*9#i03#2cy2p&z9bogb0s5sq+(cay6z!5p$8!i&2=mdqddjwa'

import sys, os
PROJECT_DIR = os.path.dirname(__file__)
#sys.path.append(PROJECT_DIR)
#sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

#TEMPLATE_LOADERS = (
#	'django.template.loaders.filesystem.load_template_source',
#	'django.template.loaders.app_directories.load_template_source',
#)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'apps.mid.GlobalRequestMiddleware',
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
	'staticfiles.context_processors.static_url',
	'context_processors.host',
	'context_processors.my_media_url',
	#'views.my_context',
	#'apps.core.views.gw_context',
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
	'objectpermissions',
#	'apps',
	'apps.*',
#	'apps.gw',
#	'apps.ref',
#	'apps.core',
#	'apps.contact',
#	'apps.file',
#	'apps.tagged',
#	'apps.task',
)

ADMIN_MEDIA_PREFIX =	'/admin_media/'
ADMIN_MEDIA_ROOT =	'/usr/lib/python2.7/site-packages/django/contrib/admin/media'

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

#from jinja.contrib import djangosupport
#djangosupport.configure()

LOGGER = True

try:
	from local_settings import *
except ImportError:
	pass
