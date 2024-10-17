from django.apps import AppConfig
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        import myapp.signals  

