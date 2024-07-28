# Generated by Django 5.0.2 on 2024-07-26 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0021_alter_harvestarea_end_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleImage",
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
                ("image", models.ImageField(upload_to="vehicle_images/")),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="drivers.vehicle",
                    ),
                ),
            ],
        ),
    ]
