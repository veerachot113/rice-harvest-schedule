# Generated by Django 5.0.2 on 2024-11-02 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0012_alter_booking_request_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='ราคา'),
        ),
    ]
