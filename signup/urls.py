from django.urls import path
from .views import CreateUserAPIView
from . import views
from .views import email_verify



urlpatterns = [
    path('test/', views.index),
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('email_verify/', views.email_verify, name='email_verify'),
    path('activate_email/<token>/<email>/', views.activate_email, name='activate_email'),
]