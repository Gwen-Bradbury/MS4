from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_gins, name='gins'),
    path('<gin_id>', views.gin_detail, name='gin_detail')
]
