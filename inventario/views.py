from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import CategoriaSerializer, ProveedorSerializer, BodegaSerializer, ProductoSerializer, MovimientoSerializer
from .models import Categoria, Proveedor, Bodega, Producto, Movimiento
from .permissions import EsAdmin, EsConsultor, PermisoMovimiento

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('api-root')
        else:
            return render(request, 'auth/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'auth/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsAdmin | EsConsultor] # autenticador segun la clase del usuario, en el caso del grupo consultor, este no puede hacer mas que mirar

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
    permission_classes = [PermisoMovimiento]  # esto es para otorgar permisos por grupo para movimientos

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