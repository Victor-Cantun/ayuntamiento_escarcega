# Generated by Django 5.1.2 on 2025-02-19 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_income', '0007_alter_category_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(unique=True, verbose_name='Banco:'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='account',
            field=models.BigIntegerField(unique=True, verbose_name='Número de cuenta:'),
        ),
        migrations.AlterField(
            model_name='category',
            name='account_number',
            field=models.CharField(unique=True, verbose_name='Número de cuenta:'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nombre de la Categoría/Ramo:'),
        ),
        migrations.AlterField(
            model_name='concept',
            name='account_number',
            field=models.CharField(unique=True, verbose_name='Número de cuenta:'),
        ),
        migrations.AlterField(
            model_name='concept',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nombre del concepto:'),
        ),
        migrations.AlterField(
            model_name='incometype',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nombre:'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='account_number',
            field=models.CharField(unique=True, verbose_name='Número de cuenta:'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(unique=True, verbose_name='Nombre de la subcategoría:'),
        ),
    ]
