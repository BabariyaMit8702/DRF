from django.apps import AppConfig


class ApappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apapp'

    def ready(self):
        from . import signals