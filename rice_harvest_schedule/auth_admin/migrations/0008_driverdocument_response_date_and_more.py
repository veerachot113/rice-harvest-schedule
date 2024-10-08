# Generated by Django 5.0.2 on 2024-07-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth_admin", "0007_alter_driverdocument_request_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="driverdocument",
            name="response_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="driverdocument",
            name="submission_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
