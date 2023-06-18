from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
# TODO Здесь нам придется переопределить сериалайзер, который использует djoser
# TODO для создания пользователя из за того, что у нас имеются нестандартные поля


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """ Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    и так же что он не может быть прочитан клиентской стороной """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    ''' Клиентская сторона не должна иметь возможность отправлять токен вместе с
    запросом на регистрацию. Сделаем его доступным только на чтение. '''
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        """ Перечислить все поля, которые могут быть включены в запрос
        или ответ, включая поля, явно указанные выше. """
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'image', 'token', 'password']

    def create(self, validated_data):
        """ Использовать метод create_user, который мы
        написали ранее, для создания нового пользователя. """
        return User.objects.create_user(**validated_data)


class CurrentUserSerializer(serializers.ModelSerializer):
    """ Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    и так же что он не может быть прочитан клиентской стороной """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    """ Клиентская сторона не должна иметь возможность отправлять токен вместе с
    запросом на регистрацию. Сделаем его доступным только на чтение. """
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        """ Перечислить все поля, которые могут быть включены в запрос
        или ответ, включая поля, явно указанные выше. """
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'image', 'token', 'last_login', ]