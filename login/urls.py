from django.urls import path
from .views import AccessTokenView,RefreshTokenView, index
from . import views

urlpatterns = [
    path('test/', views.index),

    path('access_token/', AccessTokenView.as_view(), name='verify-token'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]