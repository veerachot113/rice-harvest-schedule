# Generated by Django 5.0.2 on 2024-08-06 07:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0032_alter_vehicle_max_acres_per_day_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="calendarevent",
            name="google_event_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]