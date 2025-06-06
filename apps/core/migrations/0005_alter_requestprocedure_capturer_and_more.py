# Generated by Django 5.1.2 on 2025-01-09 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_trackingprocedure_procedure"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="requestprocedure",
            name="capturer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="request_capturer",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Capturista",
            ),
        ),
        migrations.AlterField(
            model_name="requestprocedure",
            name="current_department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Dependence",
                to="core.dependence",
                verbose_name="Departamento",
            ),
        ),
        migrations.AlterField(
            model_name="requestprocedure",
            name="procedure_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="procedures_types",
                to="core.proceduretype",
                verbose_name="Tipo de gestion",
            ),
        ),
        migrations.AlterField(
            model_name="requestprocedure",
            name="requester",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="requesters",
                to="core.citizen",
                verbose_name="Solicitante",
            ),
        ),
        migrations.AlterField(
            model_name="trackingprocedure",
            name="capturer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracking_capturer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="trackingprocedure",
            name="from_department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="from_department",
                to="core.dependence",
                verbose_name="Departamento que recibe",
            ),
        ),
        migrations.AlterField(
            model_name="trackingprocedure",
            name="to_department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="to_department",
                to="core.dependence",
                verbose_name="Departamento que emite",
            ),
        ),
    ]
