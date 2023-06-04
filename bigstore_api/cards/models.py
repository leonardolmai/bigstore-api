from django.conf import settings
from django.db.models import CASCADE, CharField, ForeignKey, Model
from django.utils.translation import gettext_lazy as _


class Card(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="user")
    name = CharField(_("Cardholder"), max_length=255, blank=False)
    number = CharField(_("Card Number"), max_length=16, blank=False)
    expiration_month = CharField(_("expiration month"), max_length=2)
    expiration_year = CharField(_("expiration Year"), max_length=4)
    cvc = CharField("CVC", max_length=4, blank=False)
