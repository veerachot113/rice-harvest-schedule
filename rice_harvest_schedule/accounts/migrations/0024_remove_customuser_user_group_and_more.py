# Generated by Django 5.0.2 on 2024-09-18 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_alter_customuser_options_alter_customuser_address_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_group',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='customuser_permissions_set', to='auth.permission'),
        ),
    ]
