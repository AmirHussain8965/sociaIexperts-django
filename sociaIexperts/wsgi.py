"""
WSGI config for sociaIexperts project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sociaIexperts.settings')

application = get_wsgi_application()
