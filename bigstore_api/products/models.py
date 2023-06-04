from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    FloatField,
    ForeignKey,
    ImageField,
    Model,
    PositiveIntegerField,
    TextField,
)
from django.utils.translation import gettext as _

from bigstore_api.users.models import Company


class Product(Model):
    CATEGORY_CHOICES = (
        ("electronics", _("Electronics")),
        ("clothing", _("Clothing")),
        ("home", _("Home")),
        ("health_beauty", _("Health and Beauty")),
        ("sports_outdoors", _("Sports and Outdoors")),
        ("books_movies_music", _("Books, Movies, and Music")),
        ("toys_games", _("Toys and Games")),
        ("automotive", _("Automotive")),
        ("furniture_home_decor", _("Furniture and Home Decor")),
        ("office_supplies", _("Office Supplies")),
    )

    name = CharField(_("Name of Product"), max_length=255)
    price = FloatField(_("price"), validators=[MinValueValidator(0.0)])
    quantity = PositiveIntegerField(_("quantity"))
    description = TextField(_("description"), blank=True, null=True)
    is_approved = BooleanField(
        _("approved"),
        default=False,
        help_text=_("Designates whether this product is approved by the large company."),
    )
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="products")
    company = ForeignKey(Company, on_delete=CASCADE, related_name="products")
    category = CharField(
        _("category"), choices=CATEGORY_CHOICES, max_length=max(len(choice[0]) for choice in CATEGORY_CHOICES)
    )


class ProductImage(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name="images")
    image = ImageField(_("image"), upload_to="products/")
