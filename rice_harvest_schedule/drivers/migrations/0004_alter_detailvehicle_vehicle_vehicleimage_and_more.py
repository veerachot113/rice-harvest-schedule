# Generated by Django 5.0.2 on 2024-06-09 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0003_remove_detailvehicle_driver_detailvehicle_vehicle_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detailvehicle",
            name="vehicle",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detail",
                to="drivers.vehicle",
            ),
        ),
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
                (
                    "image",
                    models.ImageField(
                        upload_to="vehicle_images/", verbose_name="รูปภาพเพิ่มเติม"
                    ),
                ),
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
        migrations.DeleteModel(
            name="CalendarEvent",
        ),
    ]
