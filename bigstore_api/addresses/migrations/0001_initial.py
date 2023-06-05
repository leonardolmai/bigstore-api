# Generated by Django 4.1.8 on 2023-06-04 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("postal_code", models.CharField(max_length=8, verbose_name="postal code")),
                ("uf", models.CharField(max_length=150, verbose_name="UF")),
                ("city", models.CharField(max_length=150, verbose_name="city")),
                ("neighborhood", models.CharField(max_length=150, verbose_name="neighborhood")),
                ("street", models.CharField(max_length=150, verbose_name="street")),
                ("number", models.CharField(max_length=20, verbose_name="number")),
                ("complement", models.CharField(blank=True, default="", max_length=150, verbose_name="complement")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]