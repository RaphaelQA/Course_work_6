import jwt
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from users.managers import UserManager
from django.utils.translation import gettext_lazy as _




class UserRoles(models.Model):
    USER = 'user'
    ADMIN = 'admin'
    ROLE = [(USER, USER), (ADMIN, ADMIN)]


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email'), db_index=True, max_length=60, unique=True)
    phone = models.CharField(_('phone'), max_length=12, null=False, blank=False)
    role = models.CharField(_('role'), max_length=15, choices=UserRoles.ROLE, default=UserRoles.USER)
    last_login = models.DateTimeField(_('last_login'), auto_now=True)
    image = models.ImageField(_('image'), upload_to="img_users")

    def image_(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'

    image_.short_description = 'Аватарка пользователя'
    image_.allow_tags = True

    # для корректной работы нам также необходимо
    # переопределить менеджер модели пользователя
    objects = UserManager()

    # В качестве подсказки — эти поля имеют
    # непосредственное отношение именно к нашей модели
    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        unique_together = ('email', 'phone',)

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return "{}, ({})".format(self.email, self.get_full_name())

    # Необходимые параметры для корректной работе Django
    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        Возвращает True, если у пользователя есть каждое из указанных разрешений.
        Если объект передан, он проверяет, есть ли у пользователя все необходимые
        разрешения для этого объекта.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        # return self.is_admin
        return True

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN  #

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.strftime('%S')
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    @property
    def token(self):
        """ Позволяет получить токен пользователя путем вызова user.token, вместо
        user.__generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        Returns the first_name plus the last_name, with a space in between.
        """
        # return self.username
        # return self.email
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Аналогично методу get_full_name().
        Returns the short name for the user.
        """
        # return self.username
        # return self.email
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Отправляет электронное письмо пользователю.
        :param subject: ТЕМА СООБЩЕНИЯ
        :param message: ТЕЛО САМОГО СООБЩЕНИЯ
        :param from_email: ОТ КОГО ОТПРАВЛЕНО СООБЩЕНИЕ
        :param kwargs:
        :return:
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

