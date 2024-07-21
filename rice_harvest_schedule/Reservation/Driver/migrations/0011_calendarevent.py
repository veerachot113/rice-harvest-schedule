# Generated by Django 5.0.2 on 2024-05-30 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Accounts", "0004_remove_userdriver_driver_license_and_more"),
        ("Driver", "0010_alter_vehicle_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="CalendarEvent",
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
                ("title", models.CharField(max_length=255)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Accounts.userdriver",
                    ),
                ),
            ],
        ),
    ]