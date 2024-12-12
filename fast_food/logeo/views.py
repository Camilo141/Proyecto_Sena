from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from empleados.models import Empleado, Asistencia , Domiciliario
from ventas.models import Pedido
# Si es Empleado
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import EmpleadoUpdateForm



# Create your views here.

def home(request):
    return render(request,'home.html'
        #context
)

def base(request):

    return render(request,'base.html')

# HTML empleado

def basempl(request):

    return render(request,'basempl.html')


def homempleado(request):
    return render(request,'homempleado.html'
        #context
)

# HTML empleado


@login_required
def dashboard(request):
    # Verifica si el usuario pertenece al grupo "Empleados"
    if request.user.groups.filter(name="Empleados").exists():
        return render(request, 'homempleado.html')  # Plantilla para empleados
    # Si no pertenece al grupo "Empleados", mostrar un error o redirigir a home
    return redirect('home')



#Ver Empleado


@login_required
def empleado_detalle(request):
    try:
        empleado = Empleado.objects.get(user=request.user)
    except Empleado.DoesNotExist:
        empleado = None

    if empleado:
        if request.method == 'POST':
            form = EmpleadoUpdateForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                return redirect('empleado_detalle')  # Redirige a la misma página después de guardar
        else:
            form = EmpleadoUpdateForm(instance=empleado)
    else:
        form = None

    return render(request, 'empleado/lista_empleados.html', {'empleado': empleado, 'form': form})
#Ver Asistencia

@login_required
def ver_asistencias(request):
    if not hasattr(request.user, 'empleado'):
        return HttpResponse("No tienes empleado asociado.")
    empleado = request.user.empleado
    asistencias = Asistencia.objects.filter(empleado=empleado)
    print(asistencias)  # Depuración
    return render(request, 'empleado/asistencias.html', {'asistencias': asistencias})

# ver pedido 

@login_required
def listar_pedidos(request):
    try:
        # Verificar si el usuario es un domiciliario
        empleado = request.user.empleado
        if empleado.cargo != 'domiciliario':
            return redirect('home')

        domiciliario = empleado.domiciliario
        pedidos = Pedido.objects.filter(domiciliario=domiciliario)

        # Obtener los estados de los pedidos
        estados_pedido = Pedido.ESTADO_PEDIDO

        if request.method == 'POST':
            pedido_id = request.POST.get('pedido_id')
            nuevo_estado = request.POST.get('estado')
            pedido = Pedido.objects.get(id=pedido_id, domiciliario=domiciliario)
            pedido.estado = nuevo_estado
            pedido.save()

        return render(request, 'empleado/lista_pedidos.html', {
            'pedidos': pedidos,
            'estados_pedido': estados_pedido
        })
    except Empleado.DoesNotExist:
        return redirect('home')
    except Domiciliario.DoesNotExist:
        return redirect('home')
    



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            # Redirigir según el grupo
            if user.groups.filter(name="Empleados").exists():
                return redirect('dashboard')  # Redirigir al dashboard de empleados
            return redirect('/')  # Redirigir a la página principal si no es empleado
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'logeo/login.html', {})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('/')

def registro(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            if user:
                login(request, user)
                messages.success(request, "Te has registrado correctamente")
                return redirect('/')
            else:
                messages.error(request, "Error al autenticar al usuario")
        else:
            messages.error(request, "Error en el formulario. Corrige los errores.")
    else:
        formulario = CustomUserCreationForm()
    
    return render(request, 'logeo/registro.html', {'form': formulario})


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguear al usuario automáticamente después del registro
            return redirect('/')  # Redirigir a la página principal
    else:
        form = CustomUserCreationForm()
    return render(request, 'logeo/registro.html', {'form': form})





