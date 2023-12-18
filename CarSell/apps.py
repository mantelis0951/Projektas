from django.apps import AppConfig


class CarsellConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CarSell'

    def ready(self):
        from .signals import create_profile, save_profile