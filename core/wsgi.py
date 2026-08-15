"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
print(">>> WSGI 1")

from django.core.wsgi import get_wsgi_application

print(">>> WSGI 2")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

print(">>> WSGI 3")

try:
    application = get_wsgi_application()
    print(">>> WSGI 4 - DJANGO INICIALIZADO")
except Exception as e:
    print(">>> ERRO AO INICIALIZAR DJANGO:", repr(e))
    raise
