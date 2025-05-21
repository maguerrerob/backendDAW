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
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import get_user_model

#--------------------------------GET--------------------------------

# .- Categorías
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

# .- Productos
#Productos de una categoría
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

#Retornar producto por id
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

#Búsqueda de productos por string
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
        
# .- Reseñas
# Reseñas de un producto
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
        


#--------------------------------POST--------------------------------
# Crear producto
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
    
# Segunda opción para importar productos desde CSV
class ProductCreateSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        if request.user.has_perm('tienda.add_producto'):
            print(request.data)
            file_obj = request.FILES.get('file') # Obtiene el archivo CSV
            if not file_obj:
                return Response({'error': 'No se encontró el archivo CSV.'}, status=status.HTTP_400_BAD_REQUEST)
            # Decodicar el archivo CSV a texto usando UTF-8
            decoded_file = TextIOWrapper(file_obj.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)
            try:
                diccionarioProducto = next(reader)
                categoria = int(diccionarioProducto.get('categoria'))
                nombre = diccionarioProducto.get('nombre')
                precio = diccionarioProducto.get('precio')
                stock =diccionarioProducto.get('stock')
                descripcion = diccionarioProducto.get('descripcion')
                foto = diccionarioProducto.get('foto')

                Producto.objects.create(
                    categoria=categoria,
                    nombre=nombre,
                    precio=precio,
                    stock=stock,
                    descripcion=descripcion,
                    foto=foto
                )
                return Response({"mensaje": "Producto creado correctamente."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            errors = [] # Lista de errores por fila

            serializer = ProductoSerializer(data=diccionarioProducto) # Intenta serializar los datos
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                errors.append({'errors': serializer.errors})
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # categoria = request.data.get('categoria')
            # nombre = request.data.get('nombre')
            # precio = request.data.get('precio')
            # stock = request.data.get('stock')
            # descripcion = request.data.get('descripcion')
            # foto = request.data.get('foto')

            # Producto.objects.create(
            #     categoria=categoria,
            #     nombre=nombre,
            #     precio=precio,
            #     stock=stock,
            #     descripcion=descripcion,
            #     foto=foto
            # )

            # return Response({"mensaje": "Producto creado correctamente."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No tienes permiso para crear productos."}, status=status.HTTP_403_FORBIDDEN)
        

# Crear reseña
@api_view(["POST"])
def post_resena(request):
    # Obtenemos el id del cliente a partir del usuario id
    dataCopy = request.data.copy()
    cliente = Cliente.objects.get(usuario=dataCopy["usuario"])
    dataCopy["cliente"] = cliente.id
    resenaCreateSerializer = ResenaCreateSerializer(data=dataCopy)
    if resenaCreateSerializer.is_valid():
        try:
            resenaCreateSerializer.save()
            return Response(resenaCreateSerializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(resenaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(["POST"])
# def post_compra(request):
#     data = request.data
#     try:
#         id_cliente = Cliente.objects.get(usuario=data['cliente_id'])
#         cliente = Cliente.object.get(id=id_cliente)
#         estado = Estado.objects.get(id=data['estado_id'])
#         direccion = data.get('direccion', '')
        
#         compra = Compra.objects.create(
#             cliente = cliente,
#             estado = estado,
#             direccion = direccion,
#             fecha=timezone.now(),
#             totalCompra=0
#         )
        
#         total = 0
#         for item in data['productos']:
#             producto = Producto.objects.get(id=item['id'])
#             cantidad = item['cantidad']
#             ProductoCompra.objects.create(
#                 producto = producto,
#                 compra=compra,
#                 cantidad = cantidad
#             )
#             total += producto.precio * cantidad
            
#             # Para actualizar stock
#             producto.stock -= cantidad
#             producto.save

#         compra.totalCompra = total
#         compra.save()
        
#         return Response({})



#--------------------------------PUT--------------------------------





#--------------------------------PATCH--------------------------------

# Producto
# Cambiar nombre de un producto
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



#--------------------------------DELETE--------------------------------
# Producto
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

# Reseña
@api_view(["DELETE"])
def borrar_resena(request, id):
    bol = request.user.has_perm('tienda.delete_reseña')
    print(bol)
    if request.user.has_perm('tienda.delete_reseña'):
        
        
        # Vista para eliminar una reseña
        try:
            resena = Reseña.objects.get(id=id)
            # if resena.user.cliente.id != request.user.cliente.id
            #     throw error
            # else:
            resena.delete()
            return Response({"mensaje": "Reseña eliminada correctamente."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


#--------------------------------SESIONES--------------------------------

# Obtener usuario a partir del token
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


# Registrar usuario
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