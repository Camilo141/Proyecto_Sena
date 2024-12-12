from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido, DetallePedido 
from inventario.models import Product  # Asegúrate de importar el modelo Producto
from .forms import PedidoForm, AgregarAlCarritoForm, ConfirmarPedidoForm
from logeo.forms import Cliente
from empleados.models import Domiciliario
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def inventario(request):
    return render(request, 'inventario/inventario.html')


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    
    # Obtener el cliente asociado al usuario autenticado
    cliente = get_object_or_404(Cliente, user=request.user)

    # Asignar un domiciliario predeterminado (puedes cambiar esta lógica según tus necesidades)
    domiciliario = Domiciliario.objects.first()  # Usar el primer domiciliario disponible
    
    if not domiciliario:
        messages.error(request, "No hay domiciliarios disponibles. Intenta más tarde.")
        return redirect('ver_carrito')  # Redirige al carrito con un mensaje de error

    # Obtener o crear un pedido para el cliente
    pedido, created = Pedido.objects.get_or_create(
        cliente=cliente,
        estado='Pendiente',
        defaults={
            'direccion_envio': '',
            'total': 0,
            'domiciliario': domiciliario,  # Asignar el domiciliario al crear el pedido
        }
    )
    
    # Crear o actualizar el detalle del pedido
    detalle_pedido, created = DetallePedido.objects.get_or_create(
        pedido=pedido,
        producto=producto,
        defaults={'cantidad': 1, 'precio': producto.precio}
    )
    
    if not created:
        # Si el producto ya estaba en el carrito, aumentar la cantidad
        detalle_pedido.cantidad += 1
        detalle_pedido.save()

    return redirect('ver_carrito')  # Redirige a la página del carrito


@login_required
def ver_carrito(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    pedido = Pedido.objects.filter(cliente=cliente, estado='Pendiente').first()

    detalles_pedido = []
    if pedido:
        detalles_pedido = DetallePedido.objects.filter(pedido=pedido)
        for detalle in detalles_pedido:
            detalle.subtotal = detalle.cantidad * detalle.precio

    context = {
        'pedido': pedido,
        'detalles_pedido': detalles_pedido,
    }
    return render(request, 'carrito/ver_carrito.html', context)


@login_required
def actualizar_carrito(request):
    if request.method == "POST":
        detalle_id = request.POST.get("detalle_id")
        nueva_cantidad = request.POST.get(f"cantidad_{detalle_id}")

        if detalle_id and nueva_cantidad:
            detalle = get_object_or_404(DetallePedido, id=detalle_id)
            try:
                nueva_cantidad = int(nueva_cantidad)
                if nueva_cantidad > 0:
                    detalle.cantidad = nueva_cantidad
                    detalle.subtotal = nueva_cantidad * detalle.precio
                    detalle.save()
                    messages.success(request, "Cantidad actualizada correctamente.")
                else:
                    messages.error(request, "La cantidad debe ser mayor a cero.")
            except ValueError:
                messages.error(request, "Cantidad no válida.")

    return redirect("ver_carrito")


@login_required
def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'carrito/pedido_confirmado.html', {'pedido': pedido})


def realizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.total = pedido.calcular_total()  # Calcular el total
            pedido.estado = 'Procesado'  # Cambiar el estado a procesado
            pedido.save()

            # Aquí puedes agregar lógica para vaciar el carrito o crear un nuevo pedido vacío
            # o redirigir al cliente a la página de confirmación
            return redirect('pedido_confirmado', pedido_id=pedido.id)
    else:
        form = PedidoForm(instance=pedido)

    context = {
        'pedido': pedido,
        'form': form
    }
    return render(request, 'carrito/realizar_pedido.html', context)


# ver pedido

from django.shortcuts import render, get_object_or_404
from .models import Pedido, DetallePedido
from logeo.forms import Cliente
from django.contrib.auth.decorators import login_required




def listar_pedidos_cliente(request):
    # Suponiendo que `request.user` está vinculado con un cliente
    cliente = request.user.cliente  # Ajusta esto según tu relación Cliente-Usuario
    pedidos = Pedido.objects.filter(cliente=cliente).prefetch_related('detalles__producto').select_related('domiciliario')
    
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})

