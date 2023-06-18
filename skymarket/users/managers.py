from django.contrib.auth.models import (
    BaseUserManager
)
# TODO здесь должен быть менеджер для модели Юзера.
# TODO Поищите эту информацию в рекомендациях к проекту
class UserManager(BaseUserManager):
    """
    Функция создания пользователя — в нее мы передаем обязательные поля
    """

    def create_user(self, email, first_name, last_name, phone, image, role='user', password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            image=image,
            phone=phone,
            role=role
        )
        user.is_active = False  # для активации пользователя по ссылке надо установить False по умолчанию
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, role='admin', password=None, **extra_fields):
        """
        Функция для создания суперпользователя — с ее помощью мы создаем администратора
        это можно сделать с помощью команды createsuperuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role=role
        )
        # user.is_admin = True
        user.is_active = True
        # user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
