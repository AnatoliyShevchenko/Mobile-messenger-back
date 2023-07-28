# Rest Framework
from rest_framework import serializers

# Django
from django.core.validators import (
    RegexValidator,
    EmailValidator,
)

# Local
from settings.config.conf import (
    PHONE_REGEX,
    PHONE_ERROR,
    USERNAME_VALIDATOR,
    PASSWORD_VALIDATOR,
)
from .models import Client


class AuthSerializer(serializers.Serializer):
    """Serializer for Authorization view."""

    username = serializers.CharField(
        required=True,
        validators=USERNAME_VALIDATOR
    )
    password = serializers.CharField(
        required=True,
        validators=PASSWORD_VALIDATOR
    )

    def validate(self, attrs):
        return super().validate(attrs)
    

class RegistrationSerializer(serializers.Serializer):
    """Serializer for Registration view."""

    username = serializers.CharField(
        required=True,
        validators=USERNAME_VALIDATOR
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            EmailValidator()
        ]
    )
    first_name = serializers.CharField(
        required=True
    )
    last_name = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True,
        validators=PASSWORD_VALIDATOR
    )
    repeat_password = serializers.CharField(
        required=True,
        validators=PASSWORD_VALIDATOR
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=PHONE_REGEX,
                message=PHONE_ERROR
            )
        ]
    )
    image = serializers.ImageField(
        required=False
    )

    def validate(self, data):
        password = data.get('password')
        repeat_password = data.get('repeat_password')
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')

        if Client.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )
        
        if Client.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        
        if Client.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                'Пользователь с таким phone number уже существует.'
            )

        if password == username or password == email:
            raise serializers.ValidationError(
                'Пароль должен отличаться от username и email'
            )

        if password != repeat_password:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        
        return data

    def save(self):
        validated_data = self.validated_data

        user = Client.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            image=validated_data['image'] or None
        )

        return user
    

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client. Wherever it wants."""

    class Meta:
        model = Client
        fields = (
            'username',
            'first_name',
            'last_name',
            'image'
        )

        