# Generated by Django 5.0.2 on 2024-07-27 06:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0024_alter_vehicledetail_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vehicledetail",
            name="image",
        ),
        migrations.AddField(
            model_name="vehicledetail",
            name="image1",
            field=models.ImageField(
                default="", upload_to="vehicle_images/", verbose_name="รูปภาพรถ 1"
            ),
        ),
        migrations.AddField(
            model_name="vehicledetail",
            name="image2",
            field=models.ImageField(
                default="", upload_to="vehicle_images/", verbose_name="รูปภาพรถ 2"
            ),
        ),
        migrations.AddField(
            model_name="vehicledetail",
            name="image3",
            field=models.ImageField(
                default="", upload_to="vehicle_images/", verbose_name="รูปภาพรถ 3"
            ),
        ),
    ]