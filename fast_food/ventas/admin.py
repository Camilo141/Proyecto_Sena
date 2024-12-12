import requests
from django.contrib import admin
from .models import Venta, DetallePedido, Pedido 
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.urls import path
from django.utils.html import format_html

@admin.register(Venta)
class VentaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'pedido', 'fecha_pago', 'monto', 'metodo_pago', 'boton_imprimir')
    actions = ['imprimir_recibo']

    def imprimir_recibo(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Por favor selecciona solo una venta para imprimir el recibo.")
            return

        venta = queryset.first()
        return self.generar_recibo(request, venta.id)

    imprimir_recibo.short_description = "Imprimir recibo (PDF)"

    def boton_imprimir(self, obj):
        return format_html(
            '<a class="button" href="{}">Imprimir recibo</a>',
            f"/admin/ventas/venta/{obj.id}/imprimir/"
        )

    boton_imprimir.short_description = "Imprimir Recibo"
    boton_imprimir.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:venta_id>/imprimir/', self.admin_site.admin_view(self.generar_recibo), name='venta-imprimir'),
        ]
        return custom_urls + urls

    def generar_recibo(self, request, venta_id):
        try:
            # Obtener datos locales
            venta = Venta.objects.select_related('pedido').get(id=venta_id)
            pedido = venta.pedido
            detalles = pedido.detalles.all()

            # Consumir datos desde un servicio web
            try:
                url = f"https://api.example.com/ventas/{venta_id}"  # URL del servicio web
                response = requests.get(url, timeout=10)  # Agregar tiempo de espera para evitar bloqueos

                if response.status_code == 200:
                    datos_externos = response.json()
                else:
                    datos_externos = {"error": f"Error al consumir la API: {response.status_code}"}
            except requests.RequestException as e:
                datos_externos = {"error": f"Error de red: {str(e)}"}

            # Renderizar la plantilla HTML
            html_string = render_to_string('recibo.html', {
                'venta': venta,
                'pedido': pedido,
                'detalles': detalles,
                'datos_externos': datos_externos,  # Agregar datos externos al contexto
            })

            # Generar el PDF
            pdf_file = HTML(string=html_string).write_pdf()

            # Devolver el PDF como respuesta
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="recibo_venta_{venta.id}.pdf"'
            return response
        except Venta.DoesNotExist:
            self.message_user(request, "Venta no encontrada.")
            return HttpResponse("Venta no encontrada", status=404)
        except Exception as e:
            self.message_user(request, f"Error al generar el recibo: {str(e)}")
            return HttpResponse("Error interno del servidor", status=500)
        
        

# Registro de Pedido
@admin.register(Pedido)
class PedidoAdmin(ImportExportModelAdmin):
    list_display = ('cliente', 'fecha_pedido', 'estado', 'telefono', 'direccion_envio', 'total')

class PedidoResource(resources.ModelResource):
    class Meta:
        model = Pedido
        fields = ('cliente', 'fecha_pedido', 'estado', 'telefono', 'direccion_envio', 'total')
