# Generated by Django 5.0.2 on 2024-07-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0028_remove_vehicledetail_image10_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicledetail",
            name="model",
            field=models.CharField(default="", max_length=100, verbose_name="รุ่น"),
        ),
        migrations.AlterField(
            model_name="vehicledetail",
            name="details",
            field=models.TextField(blank=True, null=True, verbose_name="รายละเอียดรถ"),
        ),
    ]