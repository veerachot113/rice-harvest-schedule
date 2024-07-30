# Generated by Django 5.0.2 on 2024-07-27 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0025_remove_vehicledetail_image_vehicledetail_image1_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicledetail",
            name="image1",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="vehicle_images/",
                verbose_name="รูปภาพรถ 1",
            ),
        ),
        migrations.AlterField(
            model_name="vehicledetail",
            name="image2",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="vehicle_images/",
                verbose_name="รูปภาพรถ 2",
            ),
        ),
        migrations.AlterField(
            model_name="vehicledetail",
            name="image3",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="vehicle_images/",
                verbose_name="รูปภาพรถ 3",
            ),
        ),
    ]