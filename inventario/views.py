from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import CategoriaSerializer, ProveedorSerializer, BodegaSerializer, ProductoSerializer, MovimientoSerializer
from .models import Categoria, Proveedor, Bodega, Producto, Movimiento
from .permissions import EsAdmin, EsConsultor, PermisoMovimiento

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

@login_required
def productos(request):
    return render(request, 'productos/productos.html')

@login_required
def movimientos(request):
    return render(request, 'movimientos/movimientos.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'auth/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'auth/register.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(username=username, email=email, password=password)
        return render(request, 'auth/login.html', {'mensaje': 'Usuario creado exitosamente'})

    return render(request, 'auth/register.html')

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsAdmin | EsConsultor]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [EsAdmin | EsConsultor]

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    permission_classes = [EsAdmin | EsConsultor]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [EsAdmin | EsConsultor]

    @action(detail=False, methods=['GET'])
    def bajo_stock(self, request):
        productos = self.get_queryset().filter(stock_actual__lte=10)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [PermisoMovimiento]  # Permisos por grupo para movimientos

    def perform_create(self, serializer):
        movimiento = serializer.save()
        producto = movimiento.producto

        if movimiento.tipo == 'ENTRADA':
            producto.stock_actual += movimiento.cantidad
        elif movimiento.tipo in ['SALIDA', 'MERMA']:
            if producto.stock_actual - movimiento.cantidad < 0:
                raise ValueError("Stock insuficiente")
            producto.stock_actual -= movimiento.cantidad

        producto.save()
# @login_required(login_url='login')
# def index(request):
#     return render(request, 'index.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             return redirect('index') # aqui redirecciona
#         else:
#             return render(request, 'auth/login.html', {'error': 'Credenciales incorrectas'})
    
#     return render(request, 'auth/login.html')

# def redirect_by_role(user): # redireccion segun el rol del usuruaio
#     if user.rol == 'admin':
#         return redirect('pantalla_admin')
#     elif user.rol == 'vendedor':
#         return redirect('pantalla_vendedor')
#     elif user.rol == 'consultor':
#         return redirect('pantalla_consultor')
#     else:
#         return redirect('index')

# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')

#         if password != password2:
#             return render(request, 'auth/register.html', {'error': 'Las contraseñas no coinciden'})

#         if User.objects.filter(username=username).exists():
#             return render(request, 'auth/register.html', {'error': 'El usuario ya existe'})

#         user = User.objects.create_user(username=username, email=email, password=password)
#         return render(request, 'auth/login.html', {'mensaje': 'Usuario creado exitosamente'})

#     return render(request, 'auth/register.html')

# def logout_view(request):
#     auth_logout(request)
#     return redirect('login')

# def listar_proveedores(request):
#     proveedores = Proveedor.objects.all()
#     serializer = ProveedorSerializer(proveedores, many=True)
#     return Response(serializer.data)

# class CategoriaViewSet(viewsets.ModelViewSet):
#     def index(request):
#         return render(request, 'templates/categorias/categoria.html')

#     queryset = Categoria.objects.all()
#     serializer_class = CategoriaSerializer
#     permission_classes = [IsAuthenticated]

# class ProveedorViewSet(viewsets.ModelViewSet):
#     def index(request):
#         return render(request, 'templates/proveedores/proveedor.html')
    
#     queryset = Proveedor.objects.all()
#     serializer_class = ProveedorSerializer
#     permission_classes = [IsAuthenticated]

# class BodegaViewSet(viewsets.ModelViewSet):
#     def index(request):
#         return render(request, 'templates/bodega/bodega.html')
    
#     queryset = Bodega.objects.all()
#     serializer_class = BodegaSerializer
#     permission_classes = [IsAuthenticated]

# class ProductoViewSet(viewsets.ModelViewSet):
#     def index(request):
#         return render(request, 'templates/productos/producto.html')
    
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer
#     permission_classes = [IsAuthenticated]
    
#     @action(detail=False, methods=['GET'])
#     def bajo_stock(self, request):
#         productos = self.get_queryset().filter(stock_actual__lte=10)
#         serializer = self.get_serializer(productos, many=True)
#         return Response(serializer.data)

# class MovimientoViewSet(viewsets.ModelViewSet):
#     def index(request):
#         return render(request, 'templates/movimientos/movimiento.html')
    
#     queryset = Movimiento.objects.all()
#     serializer_class = MovimientoSerializer
#     permission_classes = [IsAuthenticated]

#     def control_stock(self, serializer): #perform_create
#         movimiento = serializer.save()
#         producto = movimiento.producto
        
#         if movimiento.tipo == 'ENTRADA':
#             producto.stock_actual += movimiento.cantidad
#         elif movimiento.tipo in ['SALIDA', 'MERMA']:
#             producto.stock_actual -= movimiento.cantidad
        
#         producto.save()