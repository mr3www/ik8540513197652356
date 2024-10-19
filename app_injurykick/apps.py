from django.apps import AppConfig


class AppInjurykickConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_injurykick'

    def ready(self):
        import app_injurykick.signals
