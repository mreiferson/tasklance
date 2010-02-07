#!/usr/bin/python
import os, sys
sys.path.insert(0,'/Users/mreiferson/dev/tlance')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ['PYTHON_EGG_CACHE'] = '/Users/mreiferson/dev/tlance/.python-eggs'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
