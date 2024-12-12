from django.contrib import admin
from .models import Product, Categoria
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'descripcion', 'estado', 'fecha_registro_producto')
    search_fields = ('nombre',)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('nombre', 'precio', 'stock', 'descripcion', 'estado', 'fecha_registro_producto')

@admin.register(Categoria)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'descripcion')


class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        fields = ('nombre', 'descripcion')







