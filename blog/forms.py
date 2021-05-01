from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
                  'image',
                  'post_title',
                  'post_content',
                 )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
                  'comment_title',
                  'comment_content',
                 )
