from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import CASCADE, BooleanField, CharField, EmailField, ForeignKey, Model, OneToOneField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from bigstore_api.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Bigstore API.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    phone = CharField(_("phone"), max_length=14, blank=True)
    cpf = CharField("CPF", max_length=11, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

        try:
            if self.company and self.company.is_active:
                self.company.delete()
        except ObjectDoesNotExist:
            pass


class Company(Model):
    name = CharField(_("Name of Company"), max_length=255)
    cnpj = CharField("CNPJ", max_length=14, unique=True)
    website = CharField(_("website"), blank=True, max_length=255)
    owner = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="company")
    is_active = BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this company should be treated as active. "
            "Unselect this instead of deleting company."
        ),
    )

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


class UserCompany(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="companies")
    company = ForeignKey(Company, on_delete=CASCADE, related_name="users")
    is_employee = BooleanField(
        _("employee"),
        default=False,
        help_text=_("Designates whether the user is an employee or just a customer " "of the company."),
    )
