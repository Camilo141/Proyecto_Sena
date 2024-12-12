from django.urls import path
from .views import home, base, registro, dashboard , basempl, listar_pedidos
from . import views

urlpatterns = [
    path('home/', home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', base , name="base"),
    path('registro/', registro, name='registro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('empl', basempl , name="basempl"),
    #path('empleado/', views.empleado_detalle, name='empleado_detalle'),
    path('empleado/detalle/', views.empleado_detalle, name='empleado_detalle'),
    path('asistencias/', views.ver_asistencias, name='ver_asistencias'),
    path('pedidos/', listar_pedidos, name='listar_pedidos'),




    #path('asistencia/<int:id>/', views.datos_asistencia_empleado, name='datos_asistencia_empleado'),






    ]
