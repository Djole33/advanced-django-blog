from django.shortcuts import render, redirect
from .models import BlogPost, Category, Comment, Profile
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, CreateBlogPostForm, AddCommentForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

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
    # I can do it via Comment model, but since I used related_name in models.py, it is a easier way to do everything in the BlogPost class
    # comments = Comment.objects.filter(blog_post=single_post.id)
    ''' comments_len = len(single_post.comments.all()) I can also count length of comments in views.py and pass it in HTML, 
    but since I used related_name in models.py, it is a easier way to do everything in the BlogPost class '''
    
    return render(request, 'main/blog_post.html', {'single_post': single_post}) # 'comments': comments, 'comments_len':comments_len

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
            form = CreateBlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = current_user
                form.save()
                messages.success(request, 'You have successfully made a new blog post!')
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, f'{error}')
                    return redirect('home')
    else:
        messages.info(request, 'You need to be logged in first.')
        return redirect('home')

    return render(request, 'main/create_blog_post.html', {'form': form})

def update_blog_post(request, pk):
    blog_post = BlogPost.objects.get(id=pk)
    if request.user == blog_post.user:
        form = CreateBlogPostForm(instance=blog_post)
        if request.user.is_authenticated:
            if request.method == "POST":
                form = CreateBlogPostForm(request.POST, request.FILES, instance=blog_post)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'You have successfully updated your blog post!')
                    return redirect('home')
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, f'{error}')
                        return redirect('home')
        else:
            messages.info(request, 'You need to be logged in first.')
            return redirect('home')

        return render(request, 'main/update_blog_post.html', {'form': form})
    
    else:
        messages.info(request, "You didn't make this post.")
        return redirect('home')
    
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    if request.user == blog_post.user:
        if request.method == "POST":
            blog_post.delete()
            messages.success(request, 'You have successfully deleted your blog post!')
            return redirect('home')
        else:
            messages.info(request, 'You need to do that with a button!')
            return redirect('home')
    else:
        messages.info(request, "You didn't make this post.")
    return redirect('home')

def add_comment(request, pk):
    form = AddCommentForm()
    commented_post = BlogPost.objects.get(id=pk)
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = AddCommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = current_user
                form.blog_post = commented_post
                form.save()
                messages.success(request, 'You have successfully commented!')
                return redirect('blog_post', pk=pk)
            else:
                for error in list(form.errors.values()):
                    messages.error(request, f'{error}')
                    return redirect('home')
    else:
        messages.info(request, 'You need to be logged in first.')
        return redirect('home')

    return render(request, 'main/add_comment.html', {'form': form})

def like_post(request, pk):
    liked_post = get_object_or_404(BlogPost, id=pk)
    liked_post.is_liked = False
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":    
            if liked_post.likes.filter(id=current_user.id).exists():
                liked_post.likes.remove(current_user)
                liked_post.is_liked = False
                liked_post.save()
                messages.error(request, 'You disliked this blog post!')
            else:
                liked_post.likes.add(current_user)
                liked_post.is_liked = True
                liked_post.save()
                messages.success(request, 'You liked this blog post!')
            return redirect(reverse('blog_post', args=[pk]))
    else:
        messages.info(request, 'You need to be logged in first.')
        return redirect('blog_post', pk=pk)
    
    return HttpResponseRedirect(reverse('blog_post', args=[int(pk)]))

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'main/user_profile.html', {'profile': profile})
