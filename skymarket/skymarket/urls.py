from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# TODO здесь необходимо подклюючит нужные нам urls к проекту

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),
    path('admin/', admin.site.urls),
    path('api/redoc-tasks/', include("redoc.urls")),

    path('api-auth/', include('rest_framework.urls')),

    path('api/api/', include('djoser.urls')),
    path('api/api/', include('djoser.urls.authtoken')),
    path('api/api/', include('djoser.urls.jwt')),

    path('api/api/', include('ads.urls')),
    path('api/auth/', include('users.urls')),

    # === API Document ===
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)