# Generated by Django 5.1 on 2024-12-08 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
        ('inventario', '0001_initial'),
        ('logeo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True, verbose_name='Fecha del pedido')),
                ('estado', models.CharField(choices=[('Pendiente', 'pendiente'), ('En Preparación', 'en preparación'), ('Listo', 'listo'), ('Empaquetando', 'empaquetando'), ('En Camino', 'en camino'), ('Llego Pedido', 'llego pedido'), ('Entregado', 'entregado')], default='Pendiente', max_length=20, verbose_name='Estado')),
                ('ciudad', models.CharField(choices=[('Bogota', 'bogota')], max_length=20, verbose_name='ciudad')),
                ('direccion_envio', models.TextField(max_length=30, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logeo.cliente')),
                ('domiciliario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empleados.domiciliario')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.product')),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.pedido')),
            ],
            options={
                'verbose_name': 'DetallePedido',
                'verbose_name_plural': 'DetallePedidos',
                'db_table': 'detalle_pedido',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True, verbose_name='Fecha del pago')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('metodo_pago', models.CharField(choices=[('Tarjeta', 'Tarjeta'), ('Efectivo', 'Efectivo')], max_length=50, verbose_name='Método de pago')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.pedido')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'venta',
                'ordering': ['id'],
            },
        ),
    ]
