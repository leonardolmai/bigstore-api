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


class Address(Model):
    id_user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    cep = CharField("CEP", max_length=8, blank=False)  # 8 caracteres cep
    uf = CharField("UF", max_length=255, blank=False)
    city = CharField(_("City"), max_length=255, blank=False)
    address1 = CharField(_("Address 1"), max_length=255, blank=False)
    address2 = CharField(_("Address 2"), max_length=255, blank=True)