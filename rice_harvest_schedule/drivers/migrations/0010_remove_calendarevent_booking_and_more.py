# Generated by Django 5.0.2 on 2024-06-15 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0009_calendarevent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="calendarevent",
            name="booking",
        ),
        migrations.AlterField(
            model_name="calendarevent",
            name="end_time",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="calendarevent",
            name="start_time",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="calendarevent",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
