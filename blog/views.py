from django.shortcuts import (
                              render,
                              redirect,
                              reverse,
                              get_object_or_404
                             )
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
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


@login_required
def edit_comment(request, comment_id):
    """ Author Access Only """
    if not request.user.is_user:
        messages.error(request, 'Sorry, only the comment author can do that')
        return redirect(reverse('home'))
    """ Edit Comment """
    """ Prefill Form """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, 'Comment successfully updated')
            return redirect(reverse('view_blog'))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        comment_form = CommentForm(instance=comment)
        messages.info(request, f'You are editing {comment.comment_title}')

    template = 'blog/edit_comment.html'
    context = {
        'comment_form': comment_form,
        'comment': comment
    }

    return render(request, template, context)


@login_required
def delete_comment(request, comment_id):
    """ Author Access Only """
    if not request.user.is_user:
        messages.error(request, 'Sorry, only the comment author can do that')
        return redirect(reverse('home'))
    """ Delete Comment """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted')
    return redirect(reverse('view_blog'))


@login_required
def add_post(request):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Add Blog Post """
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            """ Assign Author To Comment """
            new_post.post_author = request.user
            new_post.save()
            post_form = PostForm()
            messages.success(request, 'Blog post successfully added')
            return redirect(reverse('view_blog'))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        post_form = PostForm()

    template = 'blog/add_post.html'
    context = {
        'post_form': post_form
    }

    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Edit Post """
    """ Prefill Form """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Post successfully updated')
            return redirect(reverse('blog_detail', args=[post.id]))
        else:
            messages.error(request,
                           'Error - Please check form is valid and try again.')
    else:
        post_form = PostForm(instance=post)
        messages.info(request, f'You are editing {post.post_title}')

    template = 'blog/edit_post.html'
    context = {
        'post_form': post_form,
        'post': post
    }

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """ Superuser Access Only """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, owners only function')
        return redirect(reverse('home'))
    """ Delete Post """
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    messages.success(request, 'Post deleted')
    return redirect(reverse('view_blog'))
