# -*- coding: utf-8 -*-

# Django settings for dasist project.
# Ready for development environment.
# use 'local_settings.py' to overwrite.

import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []
ADMINS = (
    ('TI_Eugene', 'ti.eugene@gmail.com'),
)
MANAGERS = ADMINS
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
# SITE_ID = 1
USE_I18N = True
USE_L10N = True
APPEND_SLASH = False
# USE_THOUSAND_SEPARATOR = True
# DECIMAL_SEPARATOR = ','
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
SECRET_KEY = 'justforme'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 86400
MAILTO = False
TESTMAIL = "user@example.com"
# urls
STATIC_URL = '/static/'
MEDIA_URL = ''
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# modules
WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'urls'
# paths
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'tmp')
LOCALE_PATHS = (os.path.join(PROJECT_DIR, 'locale'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'dasist.sqlite3'),
    }
}


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # try
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.static',
            ],
        },
    },
]

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'contrib',
    'invoice',
    'contract',
    'invarch',
    'contrarch',
    'reports',
)

AJAX_LOOKUP_CHANNELS = {
    'shipper': ('core.lookups', 'ShipperLookup')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'standard': {
            'format': "[dasist] [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'standard',
            'facility': 'user',
            # uncomment next line if rsyslog works with unix socket only (UDP reception disabled)
            # 'address': '/dev/log'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(PROJECT_DIR, 'debug.log'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'level': 'ERROR',
            'handlers': ['mail_admins'],
            'propagate': True,
        },
        '': {
            'level': 'DEBUG',   # was INFO
            'handlers': ['console'],
            'propagate': True
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass
