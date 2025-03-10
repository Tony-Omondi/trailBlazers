from django.apps import AppConfig

class KibraToursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kibraTours'

    def ready(self):
        import kibraTours.signals