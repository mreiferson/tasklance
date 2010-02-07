import os
import sys

appdir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, appdir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(appdir, '.python-eggs')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
