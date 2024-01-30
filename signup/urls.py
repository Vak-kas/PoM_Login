from django.urls import path
from .views import CreateUserAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views



urlpatterns = [
    path('test/', views.index),
    path('', CreateUserAPIView.as_view(), name='signup'),
]