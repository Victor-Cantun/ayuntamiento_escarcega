from django.apps import AppConfig


class AUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.a_users"

    def ready(self):
        import apps.a_users.signals
