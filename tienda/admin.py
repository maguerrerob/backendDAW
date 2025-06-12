from django.contrib import admin
from .models import *
from import_export import resources

# Register your models here.

misModelos = [
    Categoria,
    Producto,
    Cliente,
    Vendedor,
    Administrador,
    Usuario,
    Resena,
    Estado,
    Compra,
    Creador,
]

admin.site.register(misModelos)