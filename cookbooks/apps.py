from django.apps import AppConfig


class CookbooksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cookbooks"

    def ready(self):
        import cookbooks.signals  # noqa
