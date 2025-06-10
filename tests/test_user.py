import pytest
from django.contrib.auth import get_user_model
from tienda.models import *
from tienda.views import *
from django.utils import timezone

User = get_user_model()

@pytest.mark.asyncio
async def test_categorias(async_rf):
    request = await async_rf.get('/categorias/')
    response = obtener_categorias(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_cliente_creation():
    user = User.objects.create_user(
        username='testuser_cliente',
        password='testpassword',
        email='testuser_cliente@example.com',
        telefono='123456789',
        rol=3
    )
    assert user.username == 'testuser_cliente'

@pytest.mark.django_db
def test_user_vendedor_creation():
    user = User.objects.create_user(
        username='testuser_vendedor',
        password='testpassword',
        email='testuser_vendedor@example.com',
        telefono='123456789',
        rol=2
    )
    assert user.username == 'testuser_vendedor'

@pytest.mark.django_db
def test_user_administrador_creation():
    user = User.objects.create_user(
        username='testuser_administrador',
        password='testpassword',
        email='testuser_administrador@example.com',
        telefono='123456789',
        rol=2
    )
    assert user.username == 'testuser_administrador'

@pytest.mark.django_db
def test_create_categoria():
    categoria = Categoria.objects.create(nombre='Test Categoria')
    assert categoria.nombre == 'Test Categoria'

@pytest.mark.django_db
def test_create_estado():
    estado = Estado.objects.create(nombre='Test Estado')
    assert estado.nombre == 'Test Estado'

@pytest.mark.django_db
def test_create_producto():
    categoria = Categoria.objects.create(nombre='categoria_test')
    producto = Producto.objects.create(
        nombre='producto_test',
        precio=100.0,
        stock=10,
        categoria=categoria,
        foto='media/imageProducts/default.jpg',
        descripcion='Descripción test'
    )
    assert producto.nombre == 'producto_test'

@pytest.mark.django_db
def test_create_compra():
    cliente = Cliente.objects.create(
        usuario=User.objects.create_user(
            username='testuser_cliente',
            password='testpassword',
            email='testuser_cliente@example.com',
            telefono='123456789',
            rol=3
        )
    )
    estado = Estado.objects.create(
        nombre='Estado_test'
    )
    productos = Producto.objects.create(
        nombre='producto_test',
        precio=100.0,
        stock=10,
        categoria=Categoria.objects.create(nombre='categoria_test'),
        foto='media/imageProducts/default.jpg',
        descripcion='Descripción test'
    )
    compra = Compra.objects.create(
        cliente=cliente,
        estado=estado,
        productos=[productos],
        fecha=timezone.now(),
        totalCompra=100.0,
        ciudad='Ciudad_test',
        direccion='direccion_test',
        cod_postal='41008',
        dni='78676767S',
        nombre_completo='Nombre completo_test',
        telefono='776676767',
        email='testuser_cliente@example.com'
    )
    assert compra.fecha == timezone.now