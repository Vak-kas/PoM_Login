from django.urls import path
from .views import LoginView,user_info

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('user_info/', user_info, name='user_info'),  # 새로 추가
]