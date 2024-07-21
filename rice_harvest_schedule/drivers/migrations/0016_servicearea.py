# Generated by Django 5.0.2 on 2024-07-14 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_customuser_is_staff"),
        ("drivers", "0015_alter_calendarevent_farmer"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceArea",
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
                ("province", models.CharField(max_length=100)),
                ("district", models.CharField(max_length=100)),
                ("subdistrict", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("details", models.TextField(blank=True)),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.customuser",
                    ),
                ),
            ],
        ),
    ]