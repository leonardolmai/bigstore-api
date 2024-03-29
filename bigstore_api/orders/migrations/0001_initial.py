# Generated by Django 4.1.8 on 2023-06-06 13:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0002_product_quantity"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0004_usercompany_unique_user_company"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "is_delivered",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this order has been delivered.",
                        verbose_name="delivered",
                    ),
                ),
                (
                    "is_returned",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this order has been returned.",
                        verbose_name="returned",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="created at")),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("card", "Card"), ("pix", "Pix"), ("bank_slip", "Bank Slip")],
                        max_length=9,
                        verbose_name="payment method",
                    ),
                ),
                ("payment_details", models.TextField(verbose_name="payment details")),
                ("delivery_address", models.TextField(verbose_name="delivery address")),
                ("total", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="total")),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="orders", to="users.company"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Name of Product")),
                (
                    "price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)], verbose_name="price"
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)], verbose_name="quantity"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="order_items", to="orders.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="order_items",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.UniqueConstraint(fields=("order", "product"), name="unique_order_product"),
        ),
    ]
