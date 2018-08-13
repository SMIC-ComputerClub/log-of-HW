"""
WSGI config for hwlog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/

in same directory as manage.py, call 'gunicorn --bind ip:port hwlog.wsgi'

still have to figure out nginx and supervisor
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hwlog.settings")

application = get_wsgi_application()
