# Generated by Django 5.0.2 on 2024-07-27 05:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0023_vehicledetail_delete_vehicleimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicledetail",
            name="image",
            field=models.ImageField(
                upload_to="vehicle_Detail_Images/", verbose_name="รูปภาพรถ"
            ),
        ),
    ]
