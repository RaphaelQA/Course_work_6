from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from ads.views import AdViewSet, CommentViewSet, Logout

# TODO настройка роутов для модели
ad_router = SimpleRouter()
ad_router.register("ads", AdViewSet, basename="ads")

""" === С помощью библиотеки drf-nested-routers можно делать гибридную ссылку /api/ads/{ad_pk}/comments/ === """
comment_router = routers.NestedSimpleRouter(ad_router, "ads", lookup='ads')
comment_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(ad_router.urls)),
    path("", include(comment_router.urls)),

    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
