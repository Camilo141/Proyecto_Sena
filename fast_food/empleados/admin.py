from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Empleado, Asistencia, Domiciliario
from .views import asignar_como_empleado
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.



class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Si el usuario se agrega al grupo 'Empleados', crear el registro en la tabla Empleado
        if 'groups' in form.cleaned_data and form.cleaned_data['groups']:
            grupo_empleados = Group.objects.get(name='Empleados')
            if grupo_empleados in form.cleaned_data['groups']:
                # Llama a la función para registrar al empleado
                asignar_como_empleado(
                    obj,
                    obj.first_name,  # Nombre del usuario
                    "Ingrese el cargo",  # Cargo
                    "0000000000",  # Teléfono
                    "ingrese la direccion"  # Dirección
                )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)




@admin.register(Empleado)
class EmpleadoAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'cargo', 'telefono', 'direccion', 'fecha_contratacion')
    search_fields = ('nombre', 'cargo')

class EmpleadoResource(resources.ModelResource):
    class Meta:
        model = Empleado
        fields = ('nombre', 'cargo', 'telefono', 'direccion', 'fecha_contratacion')



@admin.register(Asistencia)
class AsistenciaAdmin(ImportExportModelAdmin):
    list_display = ('empleado', 'fecha', 'hora_entrada', 'hora_salida')
    search_fields = ('empleado__nombre',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Los superusuarios pueden ver todos los registros
        try:
            empleado = Empleado.objects.get(user=request.user)
            return qs.filter(empleado=empleado)
        except Empleado.DoesNotExist:
            return qs.none()  
        
class AsistenciaResource(resources.ModelResource):
    class Meta:
        model = Asistencia
        fields = ('empleado', 'fecha', 'hora_entrada', 'hora_salida')


@admin.register(Domiciliario)
class DomiciliarioAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'correo_electronico', 'telefono', 'estado', 'vehiculo_asignado')
    search_fields = ('nombre', 'correo_electronico', 'telefono', 'estado', 'vehiculo_asignado' )

class DomiciliarioResource(resources.ModelResource):
    class Meta:
        model = Domiciliario
        fields = ('nombre', 'correo_electronico', 'telefono', 'estado', 'vehiculo_asignado')