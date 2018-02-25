import binascii
from django.db import models
import os


class BaseModelAuditoria(models.Model):
    """
    Modelo Base para los modelos que se quiera guardar su auditoria

    Usage::

        from common.models import BaseModelAuditoria
        class Usuario(BaseModelAuditoria):
            usuario = models.CharField(max_length=20)
            other_fields = models.CharField(max_length=20)
    """

    # le pongo esta anotacion `%(app_label)s_%(class)s_usr_created` ya que las llaves foraneas, crean un identificador
    # por el cual se podra acceder a la relación, entonces la anotación que puse en related_name
    # la crea dinamicamente segun el modelo
    # si es que no se le pone, todos los modelos que implementan de `BaseModelAuditoria` tendrian el mismo identificador
    # y por lo tanto cuando se hagan las migraciones, saldria ERROR!
    usr_creacion = models.ForeignKey('Usuario', on_delete=True, related_name="%(app_label)s_%(class)s_usr_created")
    usr_modificacion = models.ForeignKey('Usuario', on_delete=True, related_name="%(app_label)s_%(class)s_usr_modified")
    usr_fecha_creacion = models.DateTimeField(auto_now_add=True)
    usr_fecha_edicion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Usuario(models.Model):
    usuario = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    nombres = models.CharField(max_length=200)
    ape_pat = models.CharField(max_length=100)
    ape_mat = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    ubigeo = models.CharField(max_length=6)
    estado = models.IntegerField()
    perfil = models.ForeignKey('Perfil', on_delete=True, )

    class Meta:
        db_table = 'PED_USUARIO'


class FormacionAcademica(BaseModelAuditoria):
    fecha_ini = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    usuario = models.ForeignKey('Usuario', on_delete=True)

    class Meta:
        db_table = 'PED_FORMACION_ACADEMICA'


class Perfil(BaseModelAuditoria):
    descripcion = models.CharField(max_length=45)
    privilegios = models.ManyToManyField('Privilegio', through='PerfilPrivilegio')

    class Meta:
        db_table = 'PED_PERFIL'


class PerfilPrivilegio(models.Model):
    perfil = models.ForeignKey('Perfil', on_delete=True, )
    privilegio = models.ForeignKey('Privilegio', on_delete=True, )

    class Meta:
        db_table = 'PED_PERFIL_PRIVILEGIO'


class Privilegio(BaseModelAuditoria):
    descripcion = models.CharField(max_length=45)
    estado = models.IntegerField()

    class Meta:
        db_table = 'PED_PRIVILEGIO'


class Token(models.Model):
    usuario = models.ForeignKey('Usuario', db_index=True, related_name='tokens', on_delete=True)
    token = models.CharField(max_length=10)
    expiration_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    # este metodo sirve para setear el token, cada vez que sea crea el registro,
    # el campo token es generado por el metodo `generate_key`
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(5)).decode()
