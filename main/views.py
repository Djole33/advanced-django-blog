from django.shortcuts import render, redirect
from .models import BlogPost, Category
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, CreateBlogPostForm
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    blogposts = BlogPost.objects.all()
    
    blogpost_name = request.GET.get('blogpost_name')

    if blogpost_name != '' and blogpost_name is not None:
        blogposts = blogposts.filter(heading__icontains=blogpost_name)

    paginator = Paginator(blogposts, 4)
    page_number = request.GET.get('page')
    blogposts = paginator.get_page(page_number)

    return render(request, 'main/home.html', {'blogposts': blogposts})

def blog_post(request, pk):
    single_post = BlogPost.objects.get(id=pk)
    return render(request, 'main/blog_post.html', {'single_post': single_post})

def categories(request):
    all_categories = Category.objects.all()
    return render(request, 'main/categories.html', {'all_categories': all_categories})

def category(request, category):
    one_category = Category.objects.get(name=category)
    category_posts = BlogPost.objects.filter(category=one_category)

    blogpost_name = request.GET.get('blogpost_name')

    if blogpost_name != '' and blogpost_name is not None:
        category_posts = category_posts.filter(heading__icontains=blogpost_name)

    paginator = Paginator(category_posts, 4)
    page_number = request.GET.get('page')
    category_posts = paginator.get_page(page_number)

    return render(request, 'main/category.html', {'one_category': one_category, 'category_posts': category_posts})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been successfully registered!'))
            return redirect('home')
        else:
            messages.error(request, ('Error registering!'))
            return redirect('register')

    else:
        return render(request, 'main/register.html', {'form': form})
      
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, ('You have been successfully logged in!'))
            return redirect('home')

        else:
            messages.error(request, ('Error logging in!'))
            return redirect('login')
    
    else:
        return render(request, 'main/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out!'))
    return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ('You have successfully changed your profile!'))
            return redirect('login')
        return render(request, 'main/update_user.html', {'user_form': user_form})
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, ('You have successfully changed your password!'))
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, f'{error}')
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'main/update_password.html', {'form': form})
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('home')

def create_blog_post(request):
    form = CreateBlogPostForm()
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = CreateBlogPostForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('You have successfully made a new blog post!'))
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, f'{error}')
                    return redirect('home')    
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('home')
    
    return render(request, 'main/create_blog_post.html', {'form': form})