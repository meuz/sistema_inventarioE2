"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'), # pagina principal donde se muestra el api root para que las personas puedan navegar, si es que no tienen permisos, al entrar en la direccion les dira que faltan persmisos, saltanto en la terminal un "GET /inventario/categorias/ HTTP/1.1" 403 o dependiendo
    path('inventario/', include('inventario.urls'), name="inventario"),
    path('inv-auth/', include('rest_framework.urls')),
]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('inventario.urls')),
# ]

# path('register/', views.register_view, name='register'),
    # path('logout/', views.logout_view, name='logout'),
    # path('productos/', views.productos, name='productos'),
    # path('movimientos/', views.movimientos, name='movimientos'),
    
    # path('index/', views.index, name='index'),