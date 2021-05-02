from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_blog, name='view_blog'),
    path('<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('addpost/', views.add_post, name='add_post')
]
