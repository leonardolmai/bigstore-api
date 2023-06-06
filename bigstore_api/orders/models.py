from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    TextField,
    UniqueConstraint,
)
from django.utils.translation import gettext as _

from bigstore_api.products.models import Product
from bigstore_api.users.models import Company


class Order(Model):
    PAYMENT_METHOD_CHOICES = (
        ("card", _("Card")),
        ("pix", _("Pix")),
        ("bank_slip", _("Bank Slip")),
    )

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="orders")
    company = ForeignKey(Company, on_delete=CASCADE, related_name="orders")
    is_delivered = BooleanField(
        _("delivered"),
        default=False,
        help_text=_("Designates whether this order has been delivered."),
    )
    is_returned = BooleanField(
        _("returned"),
        default=False,
        help_text=_("Designates whether this order has been returned."),
    )
    is_canceled = BooleanField(
        _("canceled"),
        default=False,
        help_text=_("Designates whether this order has been canceled."),
    )
    created_at = DateTimeField(_("created at"), auto_now_add=True)
    payment_method = CharField(
        _("payment method"),
        choices=PAYMENT_METHOD_CHOICES,
        max_length=max(len(choice[0]) for choice in PAYMENT_METHOD_CHOICES),
    )
    payment_details = TextField(_("payment details"))
    delivery_address = TextField(_("delivery address"))
    total = DecimalField(_("total"), max_digits=10, decimal_places=2)


class OrderItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name="order_items")
    product = ForeignKey(Product, on_delete=DO_NOTHING, related_name="order_items")
    name = CharField(_("Name of Product"), max_length=255)
    price = FloatField(_("price"), validators=[MinValueValidator(0.0)])
    quantity = PositiveIntegerField(_("quantity"), validators=[MinValueValidator(1)])


class Meta:
    constraints = [UniqueConstraint(fields=["order", "product"], name="unique_order_product")]
