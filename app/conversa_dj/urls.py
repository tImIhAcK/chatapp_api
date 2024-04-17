from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="ChatPP API",
        default_version="v1",
        description="REST implementation of ChatAPP system. The provided set of Django Rest Framework views are to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.",
        contact=openapi.Contact(email="adeniranjohn2016@gmail.com"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    re_path(
        r"^$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="chatapp_api_docs",
    ),
    path("admin/", admin.site.urls),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/auth/jwt/token/',
         CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'
         ),
    path('api/v1/auth/jwt/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

    path('api/v1/account/', include('accounts.urls')),

    path('api/v1/chats/', include('chats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MDE5NzYwLCJpYXQiOjE3MDc5MzMzNjAsImp0aSI6ImFjYWExMmQ5OTI5ODRmZWI4MzhmMGJkZjgwNDgwZjk2IiwidXNlcl9pZCI6MSwiZW1haWwiOiJhZG1pbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWN0aXZlIjp0cnVlfQ.jUuhbeWUYR-6mL9Y5KFOngUgKQYoRnoeYJ3fcAfWteE
