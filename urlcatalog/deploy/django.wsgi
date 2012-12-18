#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys
sys.path.append('/home/django-projects')
sys.path.append('/home/django-projects/urlcatalog')

os.environ['DJANGO_SETTINGS_MODULE'] = 'urlcatalog.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()