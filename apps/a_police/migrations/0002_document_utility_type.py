# Generated by Django 5.1.2 on 2025-06-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_police', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='utility_type',
            field=models.CharField(blank=True, choices=[('si', 'si'), ('no', 'no')], help_text='Sabe manejar vehículo', max_length=20, null=True),
        ),
    ]
