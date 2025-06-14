from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from import_export import resources

# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    VENDEDOR = 2
    CLIENTE = 3
    CREADOR = 4
    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'vendedor'),
        (CREADOR, 'creador'),
    )
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=1
    )
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.usuario.username

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.usuario.username
    
class Creador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.usuario.username
    
class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)

    def __str__(self):
        return self.usuario.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
def upload_path(instance, filename):
    return '/'.join(['imageProducts', str(instance.id), filename])

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField()
    foto = models.ImageField(null=True, upload_to=upload_path)

    def __str__(self):
        return self.nombre
    

    
class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ProductoCompra')
    fecha = models.DateTimeField(default=timezone.now)
    totalCompra = models.DecimalField(max_digits=10, decimal_places=2)
    ciudad = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    cod_postal = models.CharField(max_length=5, blank=True)
    dni = models.CharField(max_length=9, default=True)
    nombre_completo = models.CharField(max_length=100, default=True)
    telefono = models.CharField(max_length=9, default=True)
    email = models.EmailField(default=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cliente.usuario.username}"
    
class ProductoCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto.nombre} - {self.compra.cliente.usuario.username}"
    
class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comentario = models.TextField()
    # fecha_creacion = models.DateTimeField(default=timezone.now)
    puntuacion = models.IntegerField()
    foto = models.ImageField(upload_to='fotos/', null=True, blank=True)

    def __str__(self):
        return self.comentario
    


    
# class Compra(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
#     cantidad = models.PositiveIntegerField()
#     fecha = models.DateTimeField(default=timezone.now)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     direccion = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return f"{self.producto.nombre} - {self.cliente.usuario.username}"