from django.shortcuts import render


def view_blog(request):
    """ Returns blog.html """
    return render(request, 'blog/blog.html')
