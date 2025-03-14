from django.contrib import admin
from django.urls import path, include
from finance import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('finance.urls')),  
    path('', include('finance.urls')),  
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.user_login, name='login'),  # Страница входа
    path('register/', views.user_register, name='register'),  # Страница регистрации
    path('logout/', views.user_logout, name='logout'),  # Выход из системы
]

