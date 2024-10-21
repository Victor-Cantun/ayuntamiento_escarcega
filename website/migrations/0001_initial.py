# Generated by Django 5.1.2 on 2024-10-21 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='accounting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/accounting/', verbose_name='Documento')),
                ('creation', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='carousel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/carousel/', verbose_name='Imagen')),
                ('creation', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='director',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('profession', models.CharField(blank=True, max_length=50, null=True, verbose_name='Profesión')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('firstlastname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Primer apellido')),
                ('secondlastname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Segundo apellido')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Correo electrónico')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dirección')),
                ('cellphone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Celular')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='images/directors_profiles/', verbose_name='Imagen de perfil')),
                ('creation', models.DateTimeField(auto_now=True)),
            ],
            options={
                'permissions': [('puede_crear', 'Puede crear director'), ('puede_leer', 'Puede leer director'), ('puede_actualizar', 'Puede actualizar director'), ('puede_eliminar', 'Puede eliminar director')],
            },
        ),
        migrations.CreateModel(
            name='position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Cargo')),
            ],
        ),
        migrations.CreateModel(
            name='dependence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Dependencia:')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Correo electrónico')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dirección')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('creation', models.DateTimeField(auto_now=True)),
                ('director', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.director')),
            ],
        ),
        migrations.CreateModel(
            name='council',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('firstlastname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Primer apellido')),
                ('secondlastname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Segundo apellido')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Correo electrónico')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dirección')),
                ('cellphone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Celular')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='images/council_profiles/', verbose_name='Imagen de perfil')),
                ('creation', models.DateTimeField(auto_now=True)),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.position', verbose_name='Cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/post/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.post')),
            ],
        ),
    ]
