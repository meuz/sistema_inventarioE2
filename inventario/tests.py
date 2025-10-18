from .models import Categoria, Proveedor, Bodega, Producto, Movimiento
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group

class InventarioAPITests(APITestCase):

    def setUp(self):
        self.grupo_admin = Group.objects.create(name='admin')
        self.grupo_consultor = Group.objects.create(name='consultor')
        self.grupo_vendedor = Group.objects.create(name='vendedor') 

        self.admin_user = User.objects.create_user(username='admin_test', password='123')
        self.consultor_user = User.objects.create_user(username='consultor_test', password='123')
        self.vendedor_user = User.objects.create_user(username='vendedor_test', password='123')

        self.admin_user.groups.add(self.grupo_admin)
        self.consultor_user.groups.add(self.grupo_consultor)
        self.vendedor_user.groups.add(self.grupo_vendedor)

        self.categoria = Categoria.objects.create(nombre='Test Categoria')
        self.proveedor = Proveedor.objects.create(razon_social='Test Proveedor', rut='1-9')
        self.bodega = Bodega.objects.create(nombre='Bodega Test', ubicacion='Test')
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            sku='TEST-001',
            precio=1000,
            stock_actual=10,
            categoria=self.categoria,
            proveedor=self.proveedor
        )


    # vlidacion error de stock
    def test_stock_insuficiente_error_400(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': 11,
            'bodega': self.bodega.id,
            'observacion': 'Test de stock insuficiente'
        }

        response = self.client.post('/inventario/movimientos/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('Stock insuficiente', str(response.data))

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 10)


    # validar opreacion de stock
    def test_stock_suficiente_success_201(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': 5,
            'bodega': self.bodega.id,
            'observacion': 'Test de salida exitosa'
        }

        response = self.client.post('/inventario/movimientos/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_actual, 5)


    # validacion de permisos
    def test_consultor_no_puede_crear_producto_403(self):
        self.client.force_authenticate(user=self.consultor_user)

        data = {
            'nombre': 'Producto Ilegal',
            'sku': 'ILEGAL-001',
            'precio': 999,
            'stock_actual': 1,
            'categoria': self.categoria.id,
            'proveedor': self.proveedor.id
        }

        response = self.client.post('/inventario/productos/', data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(Producto.objects.filter(sku='ILEGAL-001').exists())


    # validacion movimiento de entrada
    def test_crear_movimiento_entrada_actualiza_stock(self):
        self.client.force_authenticate(user=self.vendedor_user)

        stock_inicial = self.producto.stock_actual
        self.assertEqual(stock_inicial, 10)

        data = {
            'producto': self.producto.id,
            'tipo': 'ENTRADA',
            'cantidad': 5,
            'bodega': self.bodega.id,
            'observacion': 'Test de entrada de stock'
        }

        response = self.client.post('/inventario/movimientos/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.producto.refresh_from_db()

        self.assertEqual(self.producto.stock_actual, 15)
    

    # validacion movimiento de salida
    def test_vendedor_puede_crear_movimiento_salida(self):
        self.client.force_authenticate(user=self.vendedor_user)

        stock_inicial = self.producto.stock_actual
        self.assertEqual(stock_inicial, 10)

        data = {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': 3,
            'bodega': self.bodega.id,
            'observacion': 'Venta realizada por vendedor_test'
        }

        response = self.client.post('/inventario/movimientos/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.producto.refresh_from_db()

        self.assertEqual(self.producto.stock_actual, 7)