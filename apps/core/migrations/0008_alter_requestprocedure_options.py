# Generated by Django 5.1.2 on 2025-01-13 00:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_alter_evidenceprocedure_procedure"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="requestprocedure",
            options={
                "permissions": [
                    ("change_status", "Puede cambiar el estado de la solicitud")
                ]
            },
        ),
    ]
