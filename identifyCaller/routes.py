from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                       # Route to the admin interface
    path('', include('identifyCallerApp.app_routes')),     # Includes app-specific URLs from identifyCallerApp
]
