# Generated by Django 5.0.2 on 2024-07-19 03:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0005_remove_booking_request_responded_by"),
        ("drivers", "0021_alter_harvestarea_end_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="harvest_area",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="drivers.harvestarea",
            ),
        ),
    ]
