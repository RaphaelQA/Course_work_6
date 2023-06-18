from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
# TODO Aдмика для пользователя - как реализовать ее можно подсмотреть в документаци django
# TODO Обычно её всегда оформляют, но в текущей задачи делать её не обязательно
@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'phone', 'role', 'image_',)
    readonly_fields = ("image_", "last_login")
    filter_horizontal = ()
    list_filter = ('role', 'email')
    list_per_page = 10
    list_max_show_all = 100