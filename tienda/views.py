from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from .forms import *
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
# from django.contrib.auth import get_user_model

# Create your views here.

@api_view(["GET"])
def list_categorias(request):
    """Vista para listar todas las categorías."""
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def list_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def returnProducto(request, id):
    producto = Producto.objects.get(id=id)
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)

# @api_view(["GET"])
# def returnmediaReseñas(request, id):
#     reseñasProducto = Reseña.objects.filter(producto=id).values_list('puntuacion', flat=True)
#     media = 0
#     for puntuacion in reseñasProducto:
#         media += puntuacion
#     media = media / len(reseñasProducto)
#     return Response({"puntuacion": media})

@api_view(["GET"])
def resenasProducto(request, id):
    reseñasProducto = Reseña.objects.filter(producto=id)
    serializer = ReseñaSerializer(reseñasProducto, many=True)
    return Response(serializer.data)

# @api_view(["POST"])
# def crear_reseña(request):
#     """Vista para crear una reseña con validación de la valoración (1 a 5)."""
#     data = request.data
    
#     # Validar que `valoracion` esté en el rango permitido
#     valoracion = data.get("valoracion", 1)
#     if not (1 <= int(valoracion) <= 5):
#         return Response({"error": "La valoración debe estar entre 1 y 5."}, status=status.HTTP_400_BAD_REQUEST)

#     # Validar existencia del producto y usuario
#     try:
#         producto = Producto.objects.get(id=data.get("producto"))
#         usuario = get_user_model().objects.get(id=data.get("usuario"))
#     except (Producto.DoesNotExist, get_user_model().DoesNotExist):
#         return Response({"error": "Producto o usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

#     # Crear y guardar la reseña
#     reseña = Reseña.objects.create(
#         producto=producto,
#         usuario=usuario,
#         comentario=data.get("comentario", ""),
#         valoracion=valoracion
#     )

#     return Response({"mensaje": "Reseña creada correctamente.", "id": reseña.id}, status=status.HTTP_201_CREATED)