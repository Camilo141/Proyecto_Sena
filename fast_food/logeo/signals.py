from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente

@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_cliente(sender, instance, **kwargs):
    instance.cliente.save()