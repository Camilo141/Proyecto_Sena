from django.db import models


# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "Categoria"
        ordering = ['id']

class Product(models.Model):

    ESTADO = (
        ('DISPONIBLE', 'Disponible'),
        ('AGOTADO', 'Agotado'),
        ('NO_DISPONIBLE', 'No disponible temporalmente'),
        ('PROMOCION', 'Promoción especial'),
    )

    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    precio = models.FloatField(verbose_name="Precio")
    Foto = models.ImageField(upload_to='img/productos/', verbose_name= "Foto")
    stock = models.IntegerField(verbose_name="Cantidad")
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO, default='DISPONIBLE')
    fecha_registro_producto = models.DateField(verbose_name="Fecha del registro", auto_now_add=True)  # Agregado auto_now_add


    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "producto"
        ordering = ['id']
        