# Generated by Django 5.1.2 on 2025-01-21 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_requestprocedure_options_alter_citizen_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestprocedure',
            name='current_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Dependence', to='core.department', verbose_name='Departamento'),
        ),
        migrations.AlterField(
            model_name='trackingprocedure',
            name='from_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_department', to='core.department', verbose_name='Departamento que recibe'),
        ),
        migrations.AlterField(
            model_name='trackingprocedure',
            name='to_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_department', to='core.department', verbose_name='Departamento que emite'),
        ),
    ]
