# Generated by Django 5.1.2 on 2025-03-04 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_income', '0009_rename_second_name_customer_maternalsurname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MethodPayment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, verbose_name='Metodo de pago:')),
            ],
        ),
        migrations.CreateModel(
            name='DetailPay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1, verbose_name='Cantidad:')),
                ('description', models.CharField(blank=True, null=True, verbose_name='Descripción:')),
                ('unit_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a_income.concept', verbose_name='Concepto')),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('no_cuenta', models.BigIntegerField(blank=True, null=True, verbose_name='Número de cuenta / Referencia bancaria:')),
                ('invoice', models.BooleanField(verbose_name='Factura:')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a_income.customer', verbose_name='Cliente:')),
                ('method_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a_income.methodpayment', verbose_name='Metodo de pago:')),
            ],
        ),
    ]
