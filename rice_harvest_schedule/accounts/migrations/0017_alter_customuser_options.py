# Generated by Django 5.0.2 on 2024-09-18 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_customuser_user_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
