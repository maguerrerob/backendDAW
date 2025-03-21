from django.contrib import admin
from .models import *

# Register your models here.

misModelos = [
    Categoria,
    Producto,
    Cliente,
    Vendedor,
    Administrador,
    Usuario,
    Reseña,
    Estado,
    Compra,
]

admin.site.register(misModelos)