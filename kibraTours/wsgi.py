"""
WSGI config for kibraTours project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kibraTours.settings')

application = get_wsgi_application()

<<<<<<< HEAD
app = application
=======
app = application
>>>>>>> b708c1804d58973abcbeac835a8a030bbd6a8608
