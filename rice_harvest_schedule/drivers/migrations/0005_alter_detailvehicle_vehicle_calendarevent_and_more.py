# Generated by Django 5.0.2 on 2024-06-09 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_driver_farmer"),
        ("drivers", "0004_alter_detailvehicle_vehicle_vehicleimage_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detailvehicle",
            name="vehicle",
            field=models.OneToOneField(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detail",
                to="drivers.vehicle",
            ),
        ),
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
                        limit_choices_to={"user_type": "driver"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.customuser",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="VehicleImage",
        ),
    ]
