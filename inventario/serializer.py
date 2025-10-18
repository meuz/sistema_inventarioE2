from rest_framework import serializers
from .models import Categoria, Proveedor, Bodega, Producto, Movimiento

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.razon_social', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'precio', 'stock_actual', 'categoria', 'proveedor', 'categoria_nombre', 'proveedor_nombre']

class MovimientoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = Movimiento
        fields = '__all__'
    
    def validate(self, data): # esta es una validacion para que el stock no quede en negativo, si es que se da el caso
        producto = data['producto']
        cantidad = data['cantidad']
        tipo = data['tipo'] 

        if tipo in ['SALIDA', 'MERMA']:
            if producto.stock_actual < cantidad:
                # 
                raise serializers.ValidationError(f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock_actual}")
        
        return data