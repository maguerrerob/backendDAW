from rest_framework import serializers
from .models import *

#--------------------------------Modelos--------------------------------

#Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

#Administrador
class AdministradorSerializer(serializers.ModelSerializer):
    # No se puede usar el serializer de Usuario porque no tiene el campo telefono
    class Meta:
        model = Administrador
        fields = '__all__'

#Cliente
class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    #No se puede usar el serializer de Usuario porque no tiene el campo telefono
    class Meta:
        model = Cliente
        fields = '__all__'

#Vendedor
class VendedorSerializer(serializers.ModelSerializer):
    #No se puede usar el serializer de Usuario porque no tiene el campo telefono
    class Meta:
        model = Vendedor
        fields = '__all__'

#Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

#Producto
class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    # foto = serializers.CharField(required=False, allow_blank=True)  # Permite que foto sea opcional
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

#Reseña
class ReseñaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    cliente = ClienteSerializer()
    class Meta:
        model = Reseña
        fields = '__all__'

#Estado
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

#ProductoCompra
class ProductoCompraSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    
    class Meta:
        model = ProductoCompra
        fields = '__all__'

#Compra
class CompraSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    estado = EstadoSerializer()
    producto = ProductoCompraSerializer(many=True, source='productocompra_set')
    
    class Meta:
        model = Compra
        fields = '__all__'






    

#--------------------------------Crear--------------------------------
class CompraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['producto', 'cliente',
                  'estado', 'cantidad',
                  'fecha', 'total',
                  'n_pedido', 'direccion']
        
class ResenaCreateSerializer(serializers.ModelSerializer):
    foto = serializers.CharField(required=False, allow_blank=True)  # Permite que foto sea opcional
    class Meta:
        model = Reseña
        fields = [
            'producto',
            'cliente',
            'puntuacion',
            'comentario',
            'foto',
        ]

    def validate_puntuacion(self, puntuacion):
        if puntuacion < 1 or puntuacion > 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return puntuacion
    
    def validate_comentario(self, comentario):
        if len(comentario) > 300:
            raise serializers.ValidationError("El comentario no puede tener más de 300 caracteres.")
        return comentario
    

# # ProductoCompra
# class ProductoCompraCreateSerializer()


#--------------------------------Update--------------------------------
class ProductoSerializerUpdateNombre(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre']

    def validate_nombre(self, nombre):
        # Para no validar si dejamos el mismo nombre de producto
        if Producto.objects.exclude(pk=self.instance.pk).filter(nombre=nombre).exists():
            raise serializers.ValidationError("El nombre del producto ya existe.")
        return nombre
    
class ProductoSerializerUpdatePrecio(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['precio']

    def validate_precio(self, precio):
        if precio <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return precio
    
class ProductoSerializerUpdateStock(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['stock']

    def validate_stock(self, stock):
        if stock < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return stock
    
    

#--------------------------------Sesiones--------------------------------

#Registro
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