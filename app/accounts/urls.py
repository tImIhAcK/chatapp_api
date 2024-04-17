from django.urls import path
from rest_framework.routers import DefaultRouter
from accounts import views


urlpatterns = [
    path('users/me/profile/', views.ProfileView.as_view(),
         name='profile-retreive-update'),
    path('activate/<str:uid>/<str:token>',
         views.ActivateUser.as_view({'post': 'activation'}),
         name='activation'),
    #     path('users/', views.UserViewSet.as_view(), name='users')
]
