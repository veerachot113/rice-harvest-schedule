# Generated by Django 5.0.2 on 2024-05-16 05:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Booking", "0008_alter_booking_farmer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]