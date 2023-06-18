from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models

from users.models import User


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(_('title'), max_length=128, name=False)
    price = models.IntegerField(_('price'), )
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to="img_goods")
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def image_(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'

    image_.short_description = 'Фото товара'
    image_.allow_tags = True

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.title)


class Comment(models.Model):
    """ Модуль хранения комментариев под объявлением """
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments_by_ad')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(_('comment_text'))
    created_at = models.DateTimeField(_('comment_create'), auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{}'.format(self.author)