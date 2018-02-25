from rest_framework import serializers
from django.contrib.auth import authenticate

from usuario.models import Usuario


class AuthSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        usuario = attrs.get('usuario')
        password = attrs.get('password')

        if usuario and password:
            user = authenticate(username=usuario, password=password)
            attrs['user'] = user
            if not user:
                msg = 'Usuario y/o contraseña invalido'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Usuario y/o contraseña requeridos'
            raise serializers.ValidationError(msg, code='authorization')

        return attrs


class AuthResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = '__all__'

    def get_token(self, data):
        return self.instance.token.token


class RequestPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_email = Usuario.objects.get(email=email)
            attrs['user'] = user_email
        except Usuario.DoesNotExist:
            msg = 'No hay ningun usuario con este correo electronico'
            raise serializers.ValidationError(msg, code='authorization')

        return attrs


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Este serializer, servira para hacer el CRUD de usuario,
    osea el ADD, UPDATE, DELETE, Y READ.
    """

    class Meta:
        model = Usuario
        fields = '__all__'
