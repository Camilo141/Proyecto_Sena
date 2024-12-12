from django.db import models
from logeo.models import Cliente
from inventario.models import Product
from empleados.models import Domiciliario

class Pedido(models.Model):
    ESTADO_PEDIDO = (
        ('Pendiente', 'pendiente'),
        ('En Preparación', 'en preparación'),
        ('Listo', 'listo'),
        ('Empaquetando', 'empaquetando'),
        ('En Camino', 'en camino'),
        ('Llego Pedido', 'llego pedido'),
        ('Entregado', 'entregado')
    )
    CIUDADES = (
                ('Bogota', 'bogota'),
    )
    domiciliario = models.ForeignKey(Domiciliario, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del pedido")
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='Pendiente', verbose_name="Estado")
    ciudad = models.CharField(max_length=20, choices=CIUDADES, verbose_name="ciudad")
    direccion_envio = models.TextField(max_length=30, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total")


    def calcular_total(self):
        total = sum(detalle.subtotal() for detalle in self.detalles.all())
        return total



    def __str__(self):
        return f"Pedido {self.id} de {self.cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = "pedido"
        ordering = ['id']


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles',null=True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')

    def subtotal(self):
        return self.cantidad * self.precio
    
    def calcular_total(self):
        total = sum(detalle.subtotal() for detalle in self.detalles.all())
        return total


    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    class Meta:
        verbose_name = "DetallePedido"
        verbose_name_plural = "DetallePedidos"
        db_table = "detalle_pedido"
        ordering = ['id']

class Venta(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')  # Corregido de 'Mondo' a 'Monto'
    metodo_pago = models.CharField(max_length=50, choices=[('Tarjeta', 'Tarjeta'), ('Efectivo', 'Efectivo')], verbose_name="Método de pago")

    def __str__(self):
        return f'Pago {self.id} - Pedido {self.pedido.id}'
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"
        ordering = ['id']

