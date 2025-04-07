from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('puntuacionReseñas/<int:id>/', views.returnmediaReseñas), # Por terminar
    path('resenasProducto/<int:id>', views.resenasProducto),
    path('obtenerUsuario/<int:token>', views.obtener_usuario_token),
    path('registrarUsuario/', views.registrar_usuario.as_view()),
    path('categorias/', views.obtener_categorias.as_view()),
    path('productos/<int:id>', views.list_productos_categoria.as_view()),
    path('producto/<int:id>', views.returnProducto.as_view()),
]