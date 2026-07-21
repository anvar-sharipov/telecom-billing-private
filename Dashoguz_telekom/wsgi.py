"""
WSGI config for Dashoguz_telekom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application
# sys.path.append(r"C:/Apache24/htdocs/Dashoguz_telekom/Dashoguz_telekom/")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashoguz_telekom.settings')

application = get_wsgi_application()
