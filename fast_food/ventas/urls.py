from django.urls import path
from . import views

urlpatterns = [
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('realizar_pedido/<int:pedido_id>/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido_confirmado/<int:pedido_id>/', views.pedido_confirmado, name='pedido_confirmado'),
    #path('ventas/<int:venta_id>/pdf/', views.SaleInvoicePdfView.as_view(), name='reporte_venta_pdf'),
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('domicilios/', views.listar_pedidos_cliente, name='listar_pedidos_cliente'),
    #path('ventas/<int:venta_id>/recibo/', views.generar_recibo, name='generar_recibo'),





    ]
