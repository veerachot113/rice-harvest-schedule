# Generated by Django 5.0.2 on 2024-06-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_admin", "0004_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="driverdocument",
            name="notification_status",
            field=models.BooleanField(default=False),
        ),
    ]
