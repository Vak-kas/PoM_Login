from django.urls import path
from .views import CreateUserAPIView
from . import views




urlpatterns = [
    path('test/', views.index),
    path('signup/', CreateUserAPIView.as_view(), name='signup'),
    path('verify-email/', views.create_and_send_verification_email, name='verify_email'),
    path('verify-code/', views.verify_code, name='verify_code'),

]