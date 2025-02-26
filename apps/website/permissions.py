from rest_framework import permissions

class CustomObjectPermissions(permissions.BasePermission):
    """
    Permisos personalizados para verificar si el usuario puede leer, crear, actualizar o eliminar
    objetos según los permisos asociados al usuario.
    """
    
    def has_permission(self, request, view):
        """
        Verifica permisos a nivel de vista.
        """
        # Verificar si es una acción de lectura (GET)
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS incluye GET, HEAD, OPTIONS
            return request.user.has_perm('mesadeatencion.puede_leer')
        
        # Verificar si es una acción de creación (POST)
        if request.method == 'POST':
            return request.user.has_perm('mesadeatencion.puede_crear')
        
        # Verificar si es una acción de actualización (PUT, PATCH)
        if request.method in ['PUT', 'PATCH']:
            return request.user.has_perm('mesadeatencion.puede_actualizar')
        
        # Verificar si es una acción de eliminación (DELETE)
        if request.method == 'DELETE':
            return request.user.has_perm('mesadeatencion.puede_eliminar')
        
        return False

    def has_object_permission(self, request, view, obj):
        """
        Verifica permisos a nivel de objeto (opcional, si necesitas controlar permisos por objeto).
        """
        # Usar las mismas reglas que en `has_permission` para acciones a nivel de objeto
        return self.has_permission(request, view)
