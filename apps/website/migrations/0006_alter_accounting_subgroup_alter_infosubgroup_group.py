# Generated by Django 5.1.2 on 2024-11-20 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_infogroup_infosubgroup_accounting_subgroup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounting",
            name="subgroup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documentos",
                to="website.infosubgroup",
            ),
        ),
        migrations.AlterField(
            model_name="infosubgroup",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subgrupos",
                to="website.infogroup",
            ),
        ),
    ]
