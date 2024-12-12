from .models import Product
from django.shortcuts import render, redirect
from ventas.models import Pedido, DetallePedido, Venta 
from inventario.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


# Create your views here.


#def inventario(request):
#    return render(request,'inventario/inventario.html' )

def lista_products(request):
    products = Product.objects.all()
    return render(request, 'inventario/inventario.html', {'products': products} )


@login_required
def crear_pedido(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    
    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        ciudad = request.POST.get('ciudad')
        
        pedido = Pedido(cliente=request.user.cliente, direccion_envio=direccion)
        pedido.save()
        
        # Guardar detalle del pedido
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=1,  # Puedes personalizar la cantidad según el formulario
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad
        )
        
        pedido.calcular_total()
        return redirect('confirmacion_pedido', pedido_id=pedido.id)
    
    return render(request, 'ventas/crear_pedido.html', {'producto': producto})


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'ventas/confirmacion_pedido.html', {'pedido': pedido})


@login_required
def registrar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        monto = request.POST.get('monto')
        metodo_pago = request.POST.get('metodo_pago')
        
        Venta.objects.create(
            pedido=pedido,
            monto=monto,
            metodo_pago=metodo_pago
        )
        
        # Actualizar estado del pedido
        pedido.estado = 'Procesado'
        pedido.save()
        
        return redirect('confirmacion_pago', venta_id=Venta.id)
    
    return render(request, 'ventas/registrar_pago.html', {'pedido': pedido})


def guardar_pedido(request):
    if request.method == 'POST':
        # lógica para guardar el pedido
        return redirect('confirmacion_pedido')
    return render(request, 'ventas/crear_pedido.html')