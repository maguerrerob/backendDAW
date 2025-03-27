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
    categoria = CategoriaSerializer(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class ReseñaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Reseña
        fields = '__all__'

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
        email = Usuario.objects.filter(email=email).first()
        if (not email is None):
            raise serializers.ValidationError("El correo ya existe.")
        return email