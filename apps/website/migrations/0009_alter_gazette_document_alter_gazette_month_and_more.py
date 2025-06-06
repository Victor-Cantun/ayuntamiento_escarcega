# Generated by Django 5.1.2 on 2024-12-17 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_remove_gazette_name_gazette_month_gazette_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gazette",
            name="document",
            field=models.FileField(
                null=True, upload_to="documents/gazette/", verbose_name="Documento"
            ),
        ),
        migrations.AlterField(
            model_name="gazette",
            name="month",
            field=models.CharField(
                choices=[
                    ("Enero", "Enero"),
                    ("Febrero", "Febrero"),
                    ("Marzo", "Marzo"),
                    ("Abril", "Abril"),
                    ("Mayo", "Mayo"),
                    ("Junio", "Junio"),
                    ("Julio", "Julio"),
                    ("Agosto", "Agosto"),
                    ("Septiembre", "Septiembre"),
                    ("Octubre", "Octubre"),
                    ("Noviembre", "Noviembre"),
                    ("Diciembre", "Diciembre"),
                ],
                max_length=20,
                null=True,
                verbose_name="Mes",
            ),
        ),
        migrations.AlterField(
            model_name="gazette",
            name="year",
            field=models.IntegerField(null=True, verbose_name="Año"),
        ),
    ]
