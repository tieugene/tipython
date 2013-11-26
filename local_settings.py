DEBUG = True
#DEBUG = False

STATIC_URL = '/static_antizapet/'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'antizapret.db'}}
#DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'antizapret', 'USER': 'antizapret', 'PASSWORD': 'antizapret',}}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}