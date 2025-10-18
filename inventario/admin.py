from django.contrib import admin
from .models import Categoria, Proveedor, Bodega, Producto, Movimiento

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'stock_actual', 'precio') # campos a mostrar
    search_fields = ('nombre', 'sku') # barra de búsqueda
    list_filter = ('categoria', 'proveedor') # filtros laterales

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Bodega)
admin.site.register(Movimiento)
