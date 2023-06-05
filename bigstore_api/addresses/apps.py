from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bigstore_api.addresses"
    verbose_name = _("Addresses")
