# Generated by Django 5.1.2 on 2025-02-04 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_requestprocedure_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestprocedure',
            name='current_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='core.department', verbose_name='Departamento'),
        ),
    ]
