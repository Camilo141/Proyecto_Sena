from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    cargo = models.CharField(max_length=20, choices=[('domiciliario', 'Domiciliario'), ('cocinero', 'Cocinero'), ('mesero', 'Mesero')])
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    direccion = models.TextField(max_length=30, verbose_name="Dirección")
    fecha_contratacion = models.DateField()

    def __str__(self):
        return self.nombre
    
    

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        db_table = "empleado"
        ordering = ['id']


class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    hora_entrada = models.TimeField(verbose_name='Hora de entrada')
    hora_salida = models.TimeField(null=True, blank=True, verbose_name='Hora de salida')

    def __str__(self):
        return f"Asistencia de {self.empleado.nombre} el {self.fecha}"

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        db_table = "asistencia"
        ordering = ['-fecha']


class Domiciliario(models.Model):
    Empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)  # Relacionar con el modelo Empleado
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('inactivo', 'Inactivo'), ('ocupado', 'Ocupado')])
    vehiculo_asignado = models.CharField(max_length=20, choices=[('moto', 'Moto'), ('bicicleta', 'Bicicleta')])  # Puede ser 'moto', 'bicicleta', etc.


    def __str__(self):
        return self.nombre
    
    

    class Meta:
        verbose_name = "Domiciliario"
        verbose_name_plural = "Domiciliarios"
        db_table = "domiciliario"
        ordering = ['id']