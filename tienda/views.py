from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from .forms import *
from django.contrib.auth.models import AbstractUser, Group
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken
from django.shortcuts import get_object_or_404
import csv
from io import TextIOWrapper

# from django.contrib.auth import get_user_model

# Vistas Públicas

class obtener_categorias(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        #Vista para listar todas las categorías
        try:
            categorias = Categoria.objects.all()
            serializer = CategoriaSerializer(categorias, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class list_productos_categoria(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        #Vista para listar productos por categoría
        try:
            categoria = Categoria.objects.get(id=id)
            productos = Producto.objects.filter(categoria=categoria)
            serializer = ProductoSerializer(productos, many=True)
            return Response(serializer.data)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class returnProducto(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        #Vista para obtener un producto por id
        try:
            producto = Producto.objects.get(id=id)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class get_busqueda_productos(APIView):
    permission_classes = [AllowAny]
    def get(self, request, string):
        #Vusta para buscar productos por nombre
        try:
            productos = Producto.objects.filter(nombre__icontains=string)
            serializers = ProductoSerializer(productos, many=True)
            return Response(serializers.data)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Importar productos desde CSV
# Espera columnas: categoria, vendedor, nombre, precio, stock, descripcion
# Opcional: foto (URL o path manejado aparte)
@api_view(["POST"])
def importarProductosCSV(request):
    if request.user.has_perm('tienda.add_producto'):
        # Verifica si el usuario tiene permiso para agregar productos
        file_obj = request.FILES.get('file') # Obtiene el archivo CSV
        if not file_obj:
            return Response({'error': 'No se encontró el archivo CSV.'}, status=status.HTTP_400_BAD_REQUEST)
        # Decodicar el archivo CSV a texto usando UTF-8
        decoded_file = TextIOWrapper(file_obj.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file) # Convierte a diccionarios por fila

        created = 0 # Contador de productos creados
        errors = [] # Lista de errores por fila

        # Iterar sobre cada fila del CSV
        for idx, row in enumerate(reader, start=1):
            try:
                categoria_id = int(row.get('categoria', '').strip()) # Obtiene el id de la categoría
                categoria = Categoria.objects.get(pk=categoria_id) # Verificar que la categoría existe
                row['categoria'] = categoria.id
            except (ValueError, KeyError, Categoria.DoesNotExist):
                errors.append({'line': idx, 'errors': f'Categoría inválida o inexistente (ID: {row.get("categoria")})'})
                continue

            serializer = ProductoSerializer(data=row) # Intenta serializar los datos
            if serializer.is_valid():
                serializer.save() # Guarda el producto si es válido
                created += 1
            else:
                errors.append({'line': idx, 'errors': serializer.errors}) # Agrega errores si hay

        result = {'created': created, 'errors': errors} # Resultado final
        status_code = status.HTTP_201_CREATED if created else status.HTTP_400_BAD_REQUEST
        return Response(result, status=status_code) # Devuelve la respuesta con el resultado
    else:
        return Response({'error': 'No tienes permiso para agregar productos.'}, status=status.HTTP_403_FORBIDDEN)


#--------------------------------Borrar producto--------------------------------

@api_view(["DELETE"])
def borrar_producto(request, id):
    if request.user.has_perm('tienda.delete_producto'):
        # Vista para eliminar un producto
        producto = Producto.objects.get(id=id)
        try:
            producto.delete()
            return Response({"mensaje": "Producto eliminado correctamente."}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "No tienes permiso para eliminar productos."}, status=status.HTTP_403_FORBIDDEN)


#---------------------------------PATCH producto--------------------------------

@api_view(["PATCH"])
def cambiarNombre_producto(request, id):
    if request.user.has_perm('tienda.change_producto'):
        # Vista para cambiar el nombre de un producto
        try:
            producto = Producto.objects.get(pk=id)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)


        serializers = ProductoSerializerUpdateNombre(instance=producto, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "No tienes permiso para cambiar el nombre del producto."}, status=status.HTTP_403_FORBIDDEN)


# Vistas de Sesiones

@api_view(["GET"])
def obtener_usuario_token(request, token):
    # Vista para obtener el usuario a partir del token
    try:
        modelotoken = AccessToken.objects.get(token=token)
        usuario = Usuario.objects.get(id=modelotoken.user_id)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegister
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegister(data=request.data)

        if serializers.is_valid():
            try:
                rol = request.data.get('rol')

                user = Usuario.objects.create_user(
                        first_name = serializers.data.get("first_name"),
                        last_name = serializers.data.get("last_name"),
                        username = serializers.data.get("username"),
                        email = serializers.data.get("email"),
                        password = serializers.data.get("password1"),
                        telefono = str(serializers.data.get("telefono")),
                        rol = rol,
                        )

                if(int(rol) == Usuario.CLIENTE):
                    grupo = Group.objects.get(id=1)
                    grupo.user_set.add(user)
                    miusuario = Cliente.objects.create( usuario = user)
                    miusuario.save()

                elif(int(rol) == Usuario.VENDEDOR):
                    grupo = Group.objects.get(id = 2)
                    grupo.user_set.add(user)
                    miusuario = Vendedor.objects.create(usuario = user)
                    miusuario.save()

                usuarioSerializado = UsuarioSerializer(user)

                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


#---------------------------------Reseñas--------------------------------

class listResenasProduct(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        # Vista para listar reseñas de un producto
        try:
            producto = Producto.objects.get(id=id)
            reseñas = Reseña.objects.filter(producto=producto)
            serializer = ReseñaSerializer(reseñas, many=True)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

api_view(["POST"])
def post_resena(request, idproducto):
    # Vista para crear una reseña
    # print(request.user)
    # if request.user.has_perm('tienda.add_reseña'):
    producto = Producto.objects.get(id=idproducto)
    # usuario = Usuario.objects.get(id=request.user.id)
    serializers = ResenaSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            resena = Reseña.create(
                producto=producto,
                # cliente=usuario,
                comentario=serializers.data.get("comentario"),
                fecha_creacion = serializers.data.get("fecha_creacion"),
                puntuacion=serializers.data.get("valoracion")
            )
            resenaSerializada = ReseñaSerializer(resena)
            return Response(resenaSerializada.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({"error": "No tienes permiso para crear reseñas."}, status=status.HTTP_403_FORBIDDEN)


#---------------------------------Compra--------------------------------
api_view(["POST"])
def comprar_producto(request):
    # if request.user.has_perm('tienda.add_compra'):
        # Vista para comprar un producto
    compraCreateSerializer = CompraCreateSerializer(data=request.data)
    if compraCreateSerializer.is_valid():
        try:
            compraCreateSerializer.save()
            return Response(compraCreateSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(compraCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


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