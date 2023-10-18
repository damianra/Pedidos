from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class RedesSociales(models.Model):
    whatsapp = models.CharField(max_length=20, null=True)
    instagram = models.CharField(max_length=200, null=True)
    faceboock = models.CharField(max_length=200, null=True)

class Rubro(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre.lower().replace(' ', '-'))
        super(Rubro, self).save(*args, **kwargs)


class Empresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, null=True)
    telefono = models.CharField(max_length=20)
    redes_sociales = models.ForeignKey(RedesSociales, on_delete=models.CASCADE, null=True)
    rubro = models.ForeignKey(Rubro, null=True, on_delete=models.CASCADE)
    horarios = models.JSONField(blank=True, null=True)
    delivery = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.nombre_empresa
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_empresa.lower().replace(' ', '-'))
        super(Empresa, self).save(*args, **kwargs)
