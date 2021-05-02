from django.shortcuts import (
                              render,
                              get_object_or_404,
                             )
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CommentForm, PostForm


def view_blog(request):
    """ Returns blog.html """
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/blog.html', context)


@login_required
def blog_detail(request, post_id):
    """ Returns blog_detail.html """
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.filter()
    new_comment = None
    template = 'blog/blog_detail.html'

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            """ Create Comment """
            new_comment = comment_form.save(commit=False)
            """ Assign Author To Comment """
            new_comment.comment_author = request.user
            new_comment.save()
            """ Assign Comment to Post """
            new_comment.post_id = post
            new_comment.save()
            comment_form = CommentForm()
            messages.success(request, 'Successfully posted your comment.')
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'on_profile_page': True
    }

    return render(request, template, context)


def add_post(request):
    """ Add a product to the store """
    postform = PostForm()
    template = 'blog/add_post.html'
    context = {
        'postform': postform,
    }

    return render(request, template, context)
