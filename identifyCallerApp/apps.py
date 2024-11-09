from django.apps import AppConfig

class IdentifyCallerAppConfig(AppConfig):
    """Configuration class for the Identify Caller application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'identifyCallerApp'
    verbose_name = "Identify Caller Application"

    def ready(self):
        """
        Override the ready method if additional startup logic is needed,
        such as registering signals.
        """
        pass
