# Generated by Django 5.1.2 on 2025-05-30 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0004_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.IntegerField(choices=[(1, 'citizen'), (2, 'employe'), (3, 'administrator'), (4, 'police')], default=1, verbose_name='Rol'),
        ),
    ]
