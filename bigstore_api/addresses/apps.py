from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bigstore_api.addresses"
    verbose_name = _("Addresses")

    def ready(self):
        try:
            import bigstore_api.addresses.signals  # noqa: F401
        except ImportError:
            pass
