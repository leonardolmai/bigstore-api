from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "bigstore_api.cards"
    verbose_name = _("Cards")

    def ready(self):
        try:
            import bigstore_api.cards.signals  # noqa: F401
        except ImportError:
            pass
