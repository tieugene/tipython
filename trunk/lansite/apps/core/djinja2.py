from django.http import HttpResponse
from django.conf import settings
from jinja2 import PackageLoader, Environment, ChoiceLoader, FileSystemLoader
import os
from django.core.urlresolvers import get_callable
#from djangotags import *
from django.utils import translation
from django.utils.thread_support import currentThread

global env

# Setup template loaders

loader_array = []
for pth in getattr(settings, 'TEMPLATE_DIRS', ()):
    loader_array.append(FileSystemLoader(pth))

for app in settings.INSTALLED_APPS:
    loader_array.append(PackageLoader(app))

# Setup environment

default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')

global_exts = getattr(settings, 'JINJA_EXTS', ())

env = Environment(extensions=global_exts, loader=ChoiceLoader(loader_array))

if 'jinja2.ext.i18n' in global_exts:
    env.install_gettext_translations(translation)

# Add user Globals, Filters, Tests
global_imports = getattr(settings, 'JINJA_GLOBALS', ())
for imp in global_imports:
    method = get_callable(imp)
    method_name = getattr(method,'jinja_name',None)
    if not method_name == None:
        env.globals[method_name] = method
    else:
        env.globals[method.__name__] = method

global_filters = getattr(settings, 'JINJA_FILTERS', ())
for imp in global_filters:
    method = get_callable(imp)
    method_name = getattr(method,'jinja_name',None)
    if not method_name == None:
        env.filters[method_name] = method
    else:
        env.filters[method.__name__] = method

global_tests = getattr(settings, 'JINJA_TESTS', ())
for imp in global_tests:
    method = get_callable(imp)
    method_name = getattr(method,'jinja_name',None)
    if not method_name == None:
        env.tests[method_name] = method
    else:
        env.tests[method.__name__] = method


def render_to_string(filename, context={}):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return rendered

def render_to_response(filename, context={}, mimetype=default_mimetype, request = None):
    if request:
        context['request'] = request
    rendered = render_to_string(filename, context)
    return HttpResponse(rendered,mimetype=mimetype)