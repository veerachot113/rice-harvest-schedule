# Generated by Django 5.0.2 on 2024-05-14 12:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Farmer", "0005_remove_booking_date_remove_booking_time_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Booking",
        ),
    ]
