# Generated by Django 5.1.2 on 2025-03-04 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0013_obligation_obligationdocument"),
    ]

    operations = [
        migrations.AddField(
            model_name="accounting",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="website.infogroup",
            ),
        ),
        migrations.AddField(
            model_name="accounting",
            name="quarter",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")],
                null=True,
                verbose_name="Trimestre",
            ),
        ),
    ]
