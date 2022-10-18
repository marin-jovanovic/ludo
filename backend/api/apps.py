from django.apps import AppConfig



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'backend.api'

    def ready(self):
        print("ready")



