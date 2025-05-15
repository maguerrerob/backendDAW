from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all()  # Valida PK de categoría
    )
    foto = serializers.CharField(required=False, allow_blank=True)  # Permite que foto sea opcional
    class Meta:
        model = Producto
        fields = [
            'id',
            'categoria',
            'nombre',
            'precio',
            'stock',
            'descripcion',
            'foto',
        ]

class ReseñaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Reseña
        fields = '__all__'

class ResenaSerializerCreate(serializers.Serializer):
    comentario = serializers.CharField()
    puntuacion = serializers.IntegerField(required=False)
    foto = serializers.CharField(required=False, allow_blank=True)  # Permite que foto sea opcional
    # fecha_creacion = serializers.DateTimeField()

    def validate_comentario(self, comentario):
        if len(comentario) > 250:
            raise serializers.ValidationError("El comentario no puede exceder los 250 carácteres.")
        return comentario
    
    def validate_puntuacion(self, puntuacion):
        if puntuacion < 0 or puntuacion > 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return puntuacion
    
    # def validate_fecha_creacion(self, fecha_creacion):
    #     if fecha_creacion > timezone.now():
    #         raise serializers.ValidationError("La fecha de creación no puede ser futura.")
    #     return fecha_creacion
    

class PuntajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reseña
        fields = ['puntuacion']

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'

class UsuarioSerializerRegister(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    telefono = serializers.CharField()  
    username = serializers.CharField()
    rol = serializers.IntegerField()
    
    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        if (not usuario is None):
            raise serializers.ValidationError("El nombre de usuario ya existe.")
        return username
    
    def validate_email(self, email):
        emailAComprobar = Usuario.objects.filter(email=email).first()
        if (not emailAComprobar is None):
            raise serializers.ValidationError("El correo ya existe.")
        return email
    
    def validate_telefono(self, telefono):
        tel = Usuario.objects.filter(telefono=telefono).first()
        if (not tel is None):
            raise serializers.ValidationError("El telefono ya existe.")
        return telefono
    

#--------------------------------Cambiar nombre producto--------------------------------
class ProductoSerializerUpdateNombre(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre']

    def validate_nombre(self, nombre):
        # Para no validar si dejamos el mismo nombre de producto
        if Producto.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise serializers.ValidationError("El nombre del producto ya existe.")
        return nombre
    
#--------------------------------Cambiar precio producto--------------------------------
class ProductoSerializerUpdatePrecio(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['precio']

    def validate_precio(self, precio):
        if precio <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return precio
    
#--------------------------------Cambiar stock producto--------------------------------
class ProductoSerializerUpdateStock(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['stock']

    def validate_stock(self, stock):
        if stock < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return stock
    

#--------------------------------Crear compra--------------------------------
class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['producto', 'cliente',
                  'estado', 'cantidad',
                  'fecha', 'total',
                  'n_pedido']