from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class TokenAuthentication(BaseAuthentication):
    """
        Simple token based authentication.

        Clients should authenticate by passing the token key in the "Authorization"
        HTTP header, prepended with the string "BYSToken ".  For example:

            Authorization: BYSToken b0ea5af778
        """

    # poner el token deseado
    keyword = 'PERUEDUCAToken'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from usuario.models import Token
        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Token invalido. Credenciales no proporcionadas.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Token invalido. El token contiene espacios en blanco'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Token invalido. El token contiene caracteres no validos'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(token=key, active=True)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token invalido')

        if not token.user.activo:
            raise exceptions.AuthenticationFailed('Usuario inactivo o eliminado.')

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
