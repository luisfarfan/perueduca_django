from django.db import models


class BaseModelAuditoria(models.Model):
    """
    Modelo Base para los modelos que se quiera guardar su auditoria

    Usage::

        from common.models import BaseModelAuditoria
        class Usuario(BaseModelAuditoria):
            usuario = models.CharField(max_length=20)
            other_fields = models.CharField(max_length=20)
    """

    usr_creacion = models.IntegerField()
    usr_modificacion = models.IntegerField()
    usr_fecha_creacion = models.DateTimeField(auto_now_add=True)
    usr_fecha_edicion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True