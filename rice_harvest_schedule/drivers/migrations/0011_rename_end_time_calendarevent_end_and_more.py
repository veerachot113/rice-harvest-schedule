# Generated by Django 5.0.2 on 2024-06-15 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_customuser_is_staff"),
        ("drivers", "0010_remove_calendarevent_booking_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="calendarevent",
            old_name="end_time",
            new_name="end",
        ),
        migrations.RenameField(
            model_name="calendarevent",
            old_name="start_time",
            new_name="start",
        ),
        migrations.AlterField(
            model_name="calendarevent",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounts.customuser"
            ),
        ),
    ]
