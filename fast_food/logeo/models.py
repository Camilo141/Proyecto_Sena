from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el modelo User
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Telefono')
    direccion = models.CharField(max_length=255, blank=True, verbose_name='Direccion')


    def __str__(self):
        return self.user.username  # Devuelve el nombre de usuario
    

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "cliente"
        ordering = ['id']
