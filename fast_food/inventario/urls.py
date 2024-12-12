from django.urls import path
from .views import lista_products, registrar_pago, confirmacion_pedido, crear_pedido, guardar_pedido 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('inventario/', lista_products, name="inventario"),
    path('confirmacion_pedido/<int:pedido_id>/', confirmacion_pedido, name='confirmacion_pedido'),
    path('registrar_pago/<int:pedido_id>/', registrar_pago, name='registrar_pago'),
    path('crear-pedido/<int:producto_id>/', crear_pedido, name='crear_pedido'),
    path('guardar-pedido/', guardar_pedido, name='guardar_pedido'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)