import os

PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Dmitriy V. Serezhin', 'sdvinfo@gmail.com'),)
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'adolat.db',}}
ALLOWED_HOSTS = []
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media_adolat/'
STATIC_ROOT = os.path.join(PROJECT_DIR,'files/collected_static/')
STATIC_URL = '/static_adolat/'
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SECRET_KEY = 's%r+ru30k%2(1v!s*1b@v)ke07m@e8_!(hat!0$*u(4nh!=-@g'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
     'django.core.context_processors.debug',
     'django.core.context_processors.i18n',
     'django.core.context_processors.media',
     'django.core.context_processors.static',
     'django.core.context_processors.request',
     'django.contrib.auth.context_processors.auth',
     'django.contrib.messages.context_processors.messages',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = os.path.join(PROJECT_DIR, 'templates')
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'reception',
    'clients',
)
CRISPY_TEMPLATE_PACK = 'bootstrap'

if DEBUG:
    TEMPLATE_STRING_IF_INVALID = ' -=Replace me to empty string=- '
else:
    TEMPLATE_STRING_IF_INVALID = ''

try:
    f=open(os.path.join(PROJECT_DIR, 'version'),'r')
    VERSION=f.read()
    f.close()
except:
    VERSION=''

try:
    from local_settings import *
except ImportError:
    pass
