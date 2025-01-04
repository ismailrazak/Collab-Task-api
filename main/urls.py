
from django.conf import settings
from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

auth_url_patterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    auth_url_patterns.append(path('verify/',include('dj_rest_auth.urls')))

api_url_patterns = [
    path('auth/', include(auth_url_patterns)),
    path('accounts/',include('users.urls')),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/',include(api_url_patterns)),
]
