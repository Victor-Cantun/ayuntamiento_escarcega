from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from allauth.account.models import EmailAddress
from .models import Document
from django.core.exceptions import ValidationError
import os
from apps.a_users.models import Profile
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(
        max_length=17, 
        required=False, 
        allow_blank=True,
        help_text="Número de teléfono (formato: +999999999)"
    )
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name','phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
    def validate_phone_number(self, value):
        """Validar formato del número de teléfono"""
        if value:
            # Remover espacios y caracteres especiales para validación
            clean_phone = value.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not clean_phone.isdigit():
                raise serializers.ValidationError("El número de teléfono solo puede contener dígitos y los símbolos +, -, (), espacios.")
            if len(clean_phone) < 9 or len(clean_phone) > 15:
                raise serializers.ValidationError("El número de teléfono debe tener entre 9 y 15 dígitos.")
        return value

    def create(self, validated_data):
        phone = validated_data.pop('phone','')
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['email'],  # Usar email como username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Crear EmailAddress para allauth
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,  # Cambiar según tu configuración
            primary=True
        )

        # Crear o actualizar perfil con teléfono
        profile,created = Profile.objects.get_or_create(user=user)
        #profile = Profile.objects.get(id=user.id)
        if phone:
            profile.phone = phone
            profile.role = 4
            profile.save()
        
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                             username=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Cuenta desactivada.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email y contraseña son requeridos.')
        
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')

#class DocumentSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Document
        #fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    file_size = serializers.SerializerMethodField()
    utility_type_display = serializers.CharField(source='get_utility_type_display', read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'type', 'type_display', 'document', 'original_name', 
                 'utility_type', 'utility_type_display','uploaded_at', 'updated_at', 'file_size']
        read_only_fields = ['uploaded_at', 'updated_at', 'original_name']
    
    def get_file_size(self, obj):
        """Retorna el tamaño del archivo en MB"""
        if obj.document:
            size_mb = obj.document.size / (1024 * 1024)
            return round(size_mb, 2)
        return 0
    
    def validate_type(self, value):
        """Validar que el tipo sea válido"""
        if value not in [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10, 11]:
            raise serializers.ValidationError("El tipo debe ser 1, 2 o 3.")
        return value
    
    def validate_document(self, value):
        """Validar tamaño y tipo de archivo"""
        if not value:
            raise serializers.ValidationError("El archivo es requerido.")
        
        # Validar tamaño (5MB = 5242880 bytes)
        if value.size > 5242880:
            raise serializers.ValidationError("El archivo no puede ser mayor a 5MB.")
        
        # Validar extensión
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.pdf':
            raise serializers.ValidationError("Solo se permiten archivos PDF.")
        
        return value
    
    def validate(self, attrs):
        """Validar que utility_type sea requerido para tipo 3"""
        document_type = attrs.get('type')
        utility_type = attrs.get('utility_type')
        
        if document_type == 7 and not utility_type:
            raise serializers.ValidationError(
                {"utility_type": "Es necesario responder la pregunta."}
            )
        
        # Limpiar utility_type si no es tipo 7
        if document_type != 7:
            attrs['utility_type'] = None
            
        return attrs    
    
    def create(self, validated_data):
        # Agregar el nombre original del archivo
        if 'document' in validated_data:
            validated_data['original_name'] = validated_data['document'].name
        
        # Verificar si ya existe un documento del mismo tipo para el usuario
        user = validated_data.get('user') or self.context['request'].user
        document_type = validated_data.get('type')
        
        existing = Document.objects.filter(user=user, type=document_type).first()
        if existing:
            raise serializers.ValidationError("Ya existe un documento de este tipo.")
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Si se actualiza el documento, eliminar el anterior y actualizar nombre
        if 'document' in validated_data and instance.document:
            old_file = instance.document.path
            if os.path.isfile(old_file):
                os.remove(old_file)
            validated_data['original_name'] = validated_data['document'].name
        
        return super().update(instance, validated_data)
    