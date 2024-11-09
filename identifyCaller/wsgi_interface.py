

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module for the 'identifyCaller' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'identifyCaller.config')

# Get the WSGI application
application = get_wsgi_application()
