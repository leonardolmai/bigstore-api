from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bigstore_api.cards"
    verbose_name = _("Cards")
