# Generated by Django 5.1.2 on 2025-01-14 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_documentprocedure_document_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryProcedure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Fecha')),
                ('comment', models.TextField(verbose_name='Se entrega')),
                ('total_amount', models.IntegerField(verbose_name='Monto final')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveries_procedures', to='core.requestprocedure')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
