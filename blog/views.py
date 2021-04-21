from django.shortcuts import render, get_object_or_404
from .models import Post, Comment


def view_blog(request):
    """ Returns blog.html """
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/blog.html', context)


def blog_detail(request, post_id):
    """ Returns blog_detail.html """
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post,
        'comments': Comment.objects.all()
    }

    return render(request, 'blog/blog_detail.html', context)
