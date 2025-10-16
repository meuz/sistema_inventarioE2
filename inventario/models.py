from django.db import models
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nombre_categoria =models.CharField(max_length=200)
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre_categoria

class Proveedor(models.Model):
    razon_social = models.TextField
    rut = models.CharField(max_length=9, unique=True) # unique para que sea unico 
    email = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return self.razon_social

class Bodega(models.Model):
    nombre_bodega = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_bodega

class Producto(models.Model):
    sku = models.CharField(max_length=12, unique=True, blank=True, editable=False) # blank para que pueda quedar en blanco en los formularios y editable false para que no se pueda ver ni editar desde el panel admiistrador
    nombre_producto = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    precio = models.IntegerField()
    stock_actual = models.IntegerField(default=0) #al ser numero enteros debemos utilizar un InterField

    def __str__(self):
        return self.nombre_producto + ' / ' + self.categoria + ' / ' + self.stock_actual 

class Movimiento(models.Model):
    # diccionario para la seleccion de tipo de movimiento
    eleccion = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('MERMA', 'Merma'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) # para proteger los datos si son borrados por casualidad
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=eleccion)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(max_length=200)

    def __str__(self):
        return self.fecha + ' / ' + self.producto + ' / ' + self.cantidad

