from django.db import models
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nombre =models.CharField(max_length=200)
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=200) 
    rut = models.CharField(max_length=9, unique=True) # unique para que sea unico 
    email = models.EmailField()
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return self.razon_social

class Bodega(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    precio = models.IntegerField()
    stock_actual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre}  / {self.categoria.nombre} / {self.sku}"

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
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)]) # para que sean numeros enteros positivos y un valor minimo de 1 para generar un moviemineto
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.tipo} / {self.cantidad} / {self.producto.nombre}"

