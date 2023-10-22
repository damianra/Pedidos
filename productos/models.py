from django.db import models
from PedidosBack.negocio.models import Empresa
from django.utils.text import slugify

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre.lower().replace(' ', '-'))
        super(Categoria, self).save(*args, **kwargs)

class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=250, null=False)
    catgoria = models.ForeignKey(Categoria, )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(blank='', default='img_default.jpg', upload_to='fotos_productos/', null=True)
    cantidad = models.PositiveIntegerField(null=False, default=1)
    promo = models.BooleanField(default=False, null=False)
    stock = models.BooleanField(default=True, null=False)

class DatosComprador(models.Model):
    nombre = models.CharField(max_length=150, null=False)
    direccion = models.CharField(max_length=250, null=False)
    entre_calles = models.CharField(max_length=250, null=True)
    telefono = models.CharField(max_length=50, null=False)

class Pedido(models.Model):
    nro_pedido = models.IntegerField(null=True)
    usuario = models.ForeignKey(DatosComprador, on_delete=models.CASCADE)
    producto = models.ManyToManyField(Producto)
