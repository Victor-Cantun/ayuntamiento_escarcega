# Generated by Django 5.1.2 on 2025-01-10 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_evidenceprocedure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidenceprocedure',
            name='procedure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images_evidence', to='core.requestprocedure'),
        ),
    ]
