# Generated by Django 5.1.2 on 2024-11-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="gazette",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=200, verbose_name="Nombre")),
                (
                    "document",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="documents/gazette/",
                        verbose_name="Documento",
                    ),
                ),
                ("creation", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
