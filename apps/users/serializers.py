from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Регистрация: уникальные логин и email, проверка сложности пароля."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            lookup='iexact',
            message='A user with this email already exists.',
        )],
    )
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'},
    )
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password2',
        ]
        read_only_fields = ['id']

    def validate_email(self, value: str) -> str:
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError(
                {'password2': 'Passwords do not match.'}
            )
        candidate = User(**{k: v for k, v in attrs.items() if k != 'password'})
        try:
            validate_password(attrs['password'], user=candidate)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Вход по логину и паролю."""

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'},
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError(
                'Invalid username or password.', code='authorization',
            )
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Публичные данные пользователя."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
