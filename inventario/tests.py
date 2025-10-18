from .models import Categoria, Proveedor, Bodega, Producto, Movimiento
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group

class InventarioAPITests(APITestCase):

    def setUp(self):
        """
        Esta función se ejecuta ANTES de cada prueba.
        Configuramos los usuarios y grupos que necesitamos.
        """
        
        # 1. Crear Grupos
        self.grupo_admin = Group.objects.create(name='admin')
        self.grupo_consultor = Group.objects.create(name='consultor')

        # 2. Crear Usuarios
        self.admin_user = User.objects.create_user(username='admin_test', password='123')
        self.consultor_user = User.objects.create_user(username='consultor_test', password='123')
        
        # 3. Asignar Usuarios a Grupos
        self.admin_user.groups.add(self.grupo_admin)
        self.consultor_user.groups.add(self.grupo_consultor)

        # 4. Crear datos de prueba (Producto, Categoria, etc.)
        self.categoria = Categoria.objects.create(nombre='Test Categoria')
        self.proveedor = Proveedor.objects.create(razon_social='Test Proveedor', rut='1-9')
        self.bodega = Bodega.objects.create(nombre='Bodega Test', ubicacion='Test')
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            sku='TEST-001',
            precio=1000,
            stock_actual=10, # <-- Stock inicial de 10
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
        """
        Prueba que un usuario 'Consultor' no puede crear (POST)
        un producto y recibe un 403 Forbidden.
        """
        # 1. Autenticar como CONSULTOR
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