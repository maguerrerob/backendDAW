from django.urls import path, re_path
from . import views

urlpatterns = [
    #----------------GET----------------
    # Listar todas las categorías
    path('categorias/', views.obtener_categorias.as_view()),
    # Productos de una categoría
    path('productos/<int:id>', views.list_productos_categoria.as_view()),
    # Retornar producto por un id
    path('producto/<int:id>', views.returnProducto.as_view()),
    # Búsqueda de productos por string
    path('productos/<str:string>', views.get_busqueda_productos.as_view()),
    # Listar reseñas de un producto
    path('listResenasProduct/<int:id>', views.listResenasProduct.as_view()),

    #----------------POST----------------
    # Importacion de productos CSV
    path('importarProductos/', views.importarProductosCSV),
    # Importar con foto
    # path('importarProductos/', views.ProductCreateSet.as_view({'post': 'create'})),
    # Crear reseña
    path('postResena/', views.post_resena),

    #----------------PUT----------------

    #----------------PATCH----------------
    # Actualizar nombre producto
    path('updateNombre/<int:id>', views.cambiarNombre_producto),
    
    #----------------DELETE----------------
    # Borrar producto
    path('delProducto/<int:id>', views.borrar_producto),
    # Borrar reseña
    path('delResena/<int:id>', views.borrar_resena),
    
    #----------------SESIONES----------------
    path('obtenerUsuario/<str:token>', views.obtener_usuario_token),
    path('registrarUsuario/', views.registrar_usuario.as_view()),
]