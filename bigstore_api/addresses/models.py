from django.conf import settings
from django.db.models import CASCADE, CharField, ForeignKey, Model
from django.utils.translation import gettext_lazy as _


class Address(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="addresses")
    postal_code = CharField(_("postal code"), max_length=8)
    uf = CharField("UF", max_length=150, blank=False)
    city = CharField(_("city"), max_length=150, blank=False)
    neighborhood = CharField(_("neighborhood"), max_length=150)
    street = CharField(_("street"), max_length=150)
    number = CharField(_("number"), max_length=20)
    complement = CharField(_("complement"), max_length=150, blank=True, default="")
