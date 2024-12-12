# views.py
from django.contrib.auth.models import Group, Permission
from .models import Empleado, Asistencia
from datetime import date
#from django.shortcuts import render



def crear_grupo_y_permisos():
    # Crear el grupo 'Empleados' si no existe
    empleados_group, created = Group.objects.get_or_create(name='Empleados')

    # Obtener o crear los permisos
    permiso_ver_asistencia, created = Permission.objects.get_or_create(codename='view_asistencia', name='Can view asistencia')

    # Asignar los permisos al grupo 'Empleados'
    empleados_group.permissions.add(permiso_ver_asistencia)

def asignar_como_empleado(usuario, nombre, cargo, telefono, direccion):
    # Asegurarse de que el grupo y los permisos estén configurados
    crear_grupo_y_permisos()

    # Obtener el grupo 'Empleados'
    grupo_empleados = Group.objects.get(name='Empleados')

    # Agregar el usuario al grupo
    usuario.groups.add(grupo_empleados)

    # Activar el permiso de staff para el usuario
    usuario.is_staff = True
    usuario.save()

    # Verificar si ya existe un registro en Empleado para evitar duplicados
    if not Empleado.objects.filter(user=usuario).exists():
        # Crear un registro en la tabla Empleado asociado al usuario
        Empleado.objects.create(
            user=usuario,
            nombre=nombre,
            cargo=cargo,
            telefono=telefono,
            direccion=direccion,
            fecha_contratacion=date.today()  # Asignamos la fecha actual de contratación
        )