from django.contrib import admin
from .models import Cliente
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.



@admin.register(Cliente)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    search_fields = ('user__username',)

class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')

