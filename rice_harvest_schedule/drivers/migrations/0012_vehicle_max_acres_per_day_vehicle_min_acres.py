# Generated by Django 5.0.2 on 2024-06-22 18:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drivers", "0011_rename_end_time_calendarevent_end_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="max_acres_per_day",
            field=models.IntegerField(
                default=25, verbose_name="จำนวนไร่สูงสุดที่เกี่ยวได้ต่อวัน (ไร่)"
            ),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="min_acres",
            field=models.IntegerField(
                default=10, verbose_name="ขั้นต่ำที่รับเกี่ยว (ไร่)"
            ),
        ),
    ]
