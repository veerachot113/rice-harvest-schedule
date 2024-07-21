# Generated by Django 5.0.2 on 2024-05-30 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Accounts", "0004_remove_userdriver_driver_license_and_more"),
        ("AuthAdmin", "0006_delete_document"),
    ]

    operations = [
        migrations.CreateModel(
            name="DriverDocument",
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
                ("document", models.FileField(upload_to="driver_documents/")),
                ("status", models.BooleanField(default=False)),
                ("cancel", models.BooleanField(default=False)),
                (
                    "driver",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Accounts.userdriver",
                    ),
                ),
            ],
        ),
    ]
