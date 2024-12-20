
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('logeo.urls')),
    path('', include('inventario.urls')),
    path('', include('ventas.urls')),
    path('', include('empleados.urls'))
    ]

    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
