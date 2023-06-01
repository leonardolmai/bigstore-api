from django.db import models
from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Card(Model):
    name = CharField(_("Cardholder"), max_length=255, blank=False)
    number = CharField(_("Card Number"),max_length=255, blank=False)
    date = CharField(_("Expiration date"), max_length=255, blank=False)
    cvc = CharField("CVC", max_length=255, blank=False)
        
        
class CardUser(Model):
    user_fk = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE,related_name="Fk_User")
    card_fk = ForeignKey(Card, on_delete=CASCADE,related_name="Fk_Card")

