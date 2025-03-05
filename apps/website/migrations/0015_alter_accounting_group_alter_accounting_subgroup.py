# Generated by Django 5.1.2 on 2025-03-04 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_accounting_group_accounting_quarter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounting',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grupos', to='website.infogroup'),
        ),
        migrations.AlterField(
            model_name='accounting',
            name='subgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgrupos', to='website.infosubgroup'),
        ),
    ]
