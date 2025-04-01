from django.urls import path, re_path
from . import views

urlpatterns = [
    path('categorias/', views.list_categorias),
    path('productos/', views.list_productos),
    path('productos/<int:id>/', views.returnProducto),
    # path('puntuacionReseñas/<int:id>/', views.returnmediaReseñas), # Por terminar
    path('resenasProducto/<int:id>', views.resenasProducto),
    # path('prueba')
    path('obtenerUsuario/<int:token>', views.obtener_usuario_token),
    path('registrarUsuario/', views.registrar_usuario.as_view()),
    path('categorias/', views.obtener_categorias),
    path('categoria/<int:id>/', views.obtener_categoria_por_id),
]