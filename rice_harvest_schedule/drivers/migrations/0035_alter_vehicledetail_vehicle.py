# Generated by Django 5.0.2 on 2024-09-12 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0034_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicledetail',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='drivers.vehicle'),
        ),
    ]
