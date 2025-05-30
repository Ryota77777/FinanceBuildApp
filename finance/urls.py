from django.contrib import admin
from django.urls import path
from finance import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🏠 Главная страница
    path('', views.home, name='home'),

    # 📁 Обзор проектов
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/stage/<int:pk>/', views.workstage_detail, name='workstage_detail'),
    path('projects/worktype/<int:pk>/', views.worktype_detail, name='worktype_detail'),

    # 🛠 Планирование
    path('planning/planning_page', views.planning_page, name='planning'),
    path('planning/project/create/', views.project_create, name='project_create'),
    path('planning/stage/create/', views.workstage_create, name='workstage_create'),
    path('planning/worktype/create/', views.worktype_create, name='worktype_create'),
    path('planning/cost/create/', views.cost_create, name='cost_create'),
    path('planning/purchase/create/', views.purchase_create, name='purchase_create'),
    path('planning/material/create', views.material_create, name='material_create'),

    # 📦 Расчёт закупок
    path('purchase_calculation/purchase_calculation_page', views.purchase_calculation_page, name='purchase_calculation'),
    path('purchase_calculation/<int:project_id>/needs/', views.material_needs, name='material_needs'),
    path('purchase_calculation/<int:project_id>/summary/', views.purchase_summary, name='purchase_summary'),

    # ⚙️ Оптимизация
    path('optimization/', views.optimization_page, name='optimization'),
    path('optimization/summary/<int:project_id>/', views.optimization_summary, name='optimization_summary'),
    path('optimization/recommendations/<int:project_id>/', views.optimization_recommendations, name='optimization_recommendations'),

    # 👤 Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]