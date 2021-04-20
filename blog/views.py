from django.shortcuts import render


def blog(request):
    """ Returns blog.html """
    return render(request, 'blog/blog.html')
