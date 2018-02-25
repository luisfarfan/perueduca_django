from django.conf import settings
from rest_framework import parsers, renderers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from usuario.models import Usuario, Token
from usuario.serializer import AuthSerializer, AuthResponseSerializer, RequestPasswordSerializer, UsuarioSerializer
from django.core.mail import send_mail


class Authenticate(APIView):
    # throttle_classes y permission_classes, sirven para decirle al djangorestframework
    # que esta APIView no hara la validación del token
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        # la data la obtengo de request.data
        # request.data lo serializo
        serializer = self.serializer_class(data=request.data)
        # aqui valido que la data sea de tipo {username, password}, como se puso en el serializer
        # además se pone raise_exception ya que la validacion la hara el serializer,
        # ya que el que controla las validaciones es el serializer. Revisar metodo validate del serializer
        serializer.is_valid(raise_exception=True)
        # si en caso el usuario y contraseña es correcto, el metodo validate del serializer,
        # devuelve el usuario logueado, para acceder a este, hacemos esto:
        user = serializer.validated_data['user']
        # creamos la fecha de expiración del token
        expiration_date = datetime.now() + timedelta(days=settings.DEFAULT_DAYS_EXPIRATION_TOKEN_REQUEST)
        token = Token.objects.get_or_create(usuario=user, active=True, expiration_date=expiration_date)
        user.token = token
        # `AuthReponseSerializer(instance=user)` este serializer recibe como instancia un objeto User,
        # para despues llamando a .data, este lo serializa para que sea un dato leido desde el front.
        return Response(AuthResponseSerializer(instance=user).data)


class RequestPassword(APIView):
    # throttle_classes y permission_classes, sirven para decirle al djangorestframework
    # que esta APIView no hara la validación del token
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RequestPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # se manda la clave por correo, faltaria implementarlo mejor, con contenido HTML personalizado
        # o con plantillas responsivas, etc, no se como se va implementar, pero no es tan complicado.
        # reference: https://docs.djangoproject.com/en/2.0/topics/email/
        send_mail(
            'Solicitud de contraseña',
            '%s' % user.password,
            'minedu@minedu.gob.pe',
            ['%s' % user.email],
            fail_silently=False,
        )
        return Response('Solicitud de envio de contraseña enviado! Revise su correo!')


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    Para poder hacer el CRUD del modelo Usuario, solo se define el queryset y serializer_class,
    y django rest framework hara su magia. No se necesita nada mas para poder hacer el CRUD.
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


authenticate = Authenticate.as_view()
request_password = RequestPassword.as_view()
