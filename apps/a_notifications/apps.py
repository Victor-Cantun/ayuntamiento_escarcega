from django.apps import AppConfig


class ANotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.a_notifications"

    def ready(self):
        import apps.a_notifications.signals
