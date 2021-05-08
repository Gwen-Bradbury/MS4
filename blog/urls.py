from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_blog, name='view_blog'),
    path('<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('addpost/', views.add_post, name='add_post'),
    path('editpost/<int:post_id>/', views.edit_post, name='edit_post'),
    path('deletepost/<int:post_id>/', views.delete_post, name='delete_post'),
    path('editcomment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('deletecomment/<int:comment_id>/',
         views.delete_comment, name='delete_comment')
]
