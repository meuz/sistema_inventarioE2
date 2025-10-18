from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProveedorViewSet, BodegaViewSet, ProductoViewSet, MovimientoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'bodegas', BodegaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# COSAS PARA PROBAR FRONT Y SINTAXIS JINJA
# urlpatterns = [
#     path('', views.index, name="index"),
#     path('categoria/', views.categoria, name="categoria"),
#     path('buscarProducto/', views.buscarProducto, name="buscarProducto"),
#     path('categorias/', views.categoria, name="categorias"),
# ]