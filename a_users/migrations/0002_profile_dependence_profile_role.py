# Generated by Django 5.1.2 on 2024-12-30 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0001_initial'),
        ('core', '0002_dependence_director_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dependence',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.dependence'),
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.IntegerField(choices=[(1, 'citizen'), (2, 'employee')], default=1, verbose_name='Rol'),
        ),
    ]
