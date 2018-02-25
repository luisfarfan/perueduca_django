from django.conf import settings
from django.contrib.auth.hashers import check_password
from .models import Usuario


class PeruEducaBackends:
    """
    Esta clase reemplaza a la authentication que tiene por defecto Django
    se puede implementar mas metodos, leer este link:
    https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#writing-an-authentication-backend
    """

    # esta funcion validara el usuario y contraseña
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and password:
            try:
                usuario = Usuario.objects.get(usuario=username, password=password)
                return usuario
            except Usuario.DoesNotExist:
                pass

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
