

import os
from django.core.asgi import get_asgi_application

# Set the settings module for the 'identifyCaller' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'identifyCaller.config')

# Get the ASGI application
application = get_asgi_application()
