from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('puntuacionReseñas/<int:id>/', views.returnmediaReseñas), # Por terminar
    path('obtenerUsuario/<str:token>', views.obtener_usuario_token),
    path('registrarUsuario/', views.registrar_usuario.as_view()),
    path('categorias/', views.obtener_categorias.as_view()),
    path('productos/<int:id>', views.list_productos_categoria.as_view()),
    path('producto/<int:id>', views.returnProducto.as_view()),
    # Búsqueda de productos por string
    path('productos/<str:string>', views.get_busqueda_productos.as_view()),
    # Importacion de productos CSV
    path('importarProductos/', views.importarProductosCSV),
    # Borrar producto
    path('delProducto/<int:id>', views.borrar_producto),
    # Actualizar nombre producto
    path('updateNombre/<int:id>', views.cambiarNombre_producto),
    #--------Reseñas--------
    path('listResenasProduct/<int:id>', views.listResenasProduct.as_view()),
    path('postResena/<int:id>', views.post_resena),
    #--------Compra---------
    path('comprarProducto/', views.comprar_producto)
]

