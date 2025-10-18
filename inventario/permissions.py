from rest_framework import permissions

class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

class EsConsultor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated and request.user.groups.filter(name='Consultor').exists()
        return False

class PermisoMovimiento(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name='Admin').exists():
            return True

        if request.user.groups.filter(name='Consultor').exists():
            return request.method in permissions.SAFE_METHODS

        if request.user.groups.filter(name='Vendedor').exists():
            return request.method in ['GET', 'POST', 'HEAD', 'OPTIONS']
        
        return False