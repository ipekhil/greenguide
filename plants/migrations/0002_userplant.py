# Generated by Django 4.2.21 on 2025-05-27 14:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("plants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserPlant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        help_text="Give your plant a name!", max_length=100
                    ),
                ),
                ("last_watered", models.DateField(default=datetime.date.today)),
                ("last_fertilized", models.DateField(default=datetime.date.today)),
                (
                    "plant_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plants.planttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
