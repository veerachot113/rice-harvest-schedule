# Generated by Django 5.0.2 on 2024-07-29 06:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_admin", "0006_remove_driverdocument_notification_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driverdocument",
            name="request_status",
            field=models.CharField(default="รอดำเนินการ", max_length=30),
        ),
    ]
