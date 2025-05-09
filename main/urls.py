from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import GoogleLoginView

auth_url_patterns = [
    path("", include("dj_rest_auth.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
]


api_url_patterns = [
    path("auth/", include(auth_url_patterns)),
    path("accounts/", include("users.urls")),
    path("houses/", include("house.urls")),
    path("tasks/", include("tasks.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_url_patterns)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    auth_url_patterns.append(path("verify/", include("rest_framework.urls")))
