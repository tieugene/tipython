import sys, os
PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True
MEDIA_ROOT = '/mnt/shares/testwdp'
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = '0mj#8oti+&amp;)y88nop+6brl&amp;5+hffwli0h@&amp;zbmi3^5tgcjxvcn'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'testwdp.urls'
WSGI_APPLICATION = 'testwdp.wsgi.application'
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testwdp',
)
try:
        from local_settings import *
except ImportError:
        pass
#print 'settings loaded'
