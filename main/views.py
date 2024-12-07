from django.shortcuts import render
from .models import BlogPost, Category

# Create your views here.

def home(request):
    blogposts = BlogPost.objects.all()
    return render(request, 'main/home.html', {'blogposts': blogposts})

def blog_post(request, pk):
    single_post = BlogPost.objects.get(id=pk)
    return render(request, 'main/blog_post.html', {'single_post': single_post})

def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'main/categories.html', {'all_categories': all_categories})

def category(request, category):
    one_category = Category.objects.get(name=category)
    return render(request, 'main/category.html', {'one_category': one_category})
