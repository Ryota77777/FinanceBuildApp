from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.user_login, name='login'),  # Страница входа
    path('register/', views.user_register, name='register'),  # Страница регистрации
    path('logout/', views.user_logout, name='logout'),  # Выход из системы
]
