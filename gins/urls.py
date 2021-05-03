from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_gins, name='gins'),
    path('<int:gin_id>/', views.gin_detail, name='gin_detail'),
    path('addgin/', views.add_gin, name='add_gin'),
    path('edit/<int:gin_id>/', views.edit_gin, name='edit_gin')
]
