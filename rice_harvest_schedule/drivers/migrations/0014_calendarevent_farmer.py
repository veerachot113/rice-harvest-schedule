# Generated by Django 5.0.2 on 2024-07-06 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0013_alter_calendarevent_end_alter_calendarevent_start"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="calendarevent",
            name="farmer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
