# Generated by Django 5.1 on 2024-12-06 03:10

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
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('cargo', models.CharField(choices=[('domiciliario', 'Domiciliario'), ('cocinero', 'Cocinero'), ('mesero', 'Mesero')], max_length=20)),
                ('telefono', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('direccion', models.TextField(max_length=30, verbose_name='Dirección')),
                ('fecha_contratacion', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'empleado',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Domiciliario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('estado', models.CharField(choices=[('disponible', 'Disponible'), ('inactivo', 'Inactivo'), ('ocupado', 'Ocupado')], max_length=20)),
                ('vehiculo_asignado', models.CharField(choices=[('moto', 'Moto'), ('bicicleta', 'Bicicleta')], max_length=20)),
                ('Empleado', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado')),
            ],
            options={
                'verbose_name': 'Domiciliario',
                'verbose_name_plural': 'Domiciliarios',
                'db_table': 'domiciliario',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('hora_entrada', models.TimeField(verbose_name='Hora de entrada')),
                ('hora_salida', models.TimeField(blank=True, null=True, verbose_name='Hora de salida')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
                'db_table': 'asistencia',
                'ordering': ['-fecha'],
            },
        ),
    ]
