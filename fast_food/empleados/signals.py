from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
#CrearGrupo

@receiver(post_migrate)
def create_empleados_group(sender, **kwargs):
    # Crea el grupo 'Empleados' si no existe
    Group.objects.get_or_create(name='Empleados')


# Domiciliarios


from django.db.models.signals import post_save
#from django.dispatch import receiver
from .models import Empleado, Domiciliario

@receiver(post_save, sender=Empleado)
def create_or_delete_domiciliario(sender, instance, created, **kwargs):
    """
    Crea un registro en la tabla Domiciliario si el cargo del empleado cambia a 'domiciliario'.
    Elimina el registro si el cargo cambia a otro valor.
    """
    if instance.cargo == 'domiciliario':
        # Verificar si ya existe un registro en Domiciliario para este empleado
        domiciliario, domiciliario_created = Domiciliario.objects.get_or_create(
            Empleado=instance,  # Relación con el modelo Empleado
            defaults={
                "nombre": instance.nombre,
                "correo_electronico": instance.user.email,  # Usa el email del usuario
                "telefono": instance.telefono,
                "estado": "disponible",  # Valor predeterminado
                "vehiculo_asignado": "moto",  # Valor predeterminado
            }
        )
        if domiciliario_created:
            print(f"Registro creado en Domiciliario para {instance.nombre}.")
        else:
            print(f"{instance.nombre} ya tiene un registro en Domiciliario.")
    else:
        # Si el cargo no es "domiciliario", eliminar el registro en Domiciliario si existe
        try:
            domiciliario = Domiciliario.objects.get(Empleado=instance)
            domiciliario.delete()
            print(f"Registro eliminado de Domiciliario para {instance.nombre}.")
        except Domiciliario.DoesNotExist:
            pass


