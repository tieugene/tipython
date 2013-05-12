import os
import sys

sys.path.append('/usr/share')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lansite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
