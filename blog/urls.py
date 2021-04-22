from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_blog, name='view_blog'),
    path('<post_id>', views.blog_detail, name='blog_detail'),
]
