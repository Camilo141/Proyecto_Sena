from django.apps import AppConfig


class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logeo'

    def ready(self):
        import logeo.signals  # Importar señales