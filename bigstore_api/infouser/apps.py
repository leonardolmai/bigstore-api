'''from django.apps import AppConfig


class InfouserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "infouser"'''
    
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bigstore_api.infouser"
    verbose_name = _("Users")

    def ready(self):
        try:
            import bigstore_api.infouser.signals  # noqa: F401
        except ImportError:
            pass
