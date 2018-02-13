from django.apps import AppConfig


class MealsConfig(AppConfig):
    name = 'meals'

    def ready(self):
        from meals import signals
