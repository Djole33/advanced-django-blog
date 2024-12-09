from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('blog_post/<int:pk>/', views.blog_post, name="blog_post"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:category>/', views.category, name="category"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('update_password/', views.update_password, name="update_password"),
    path('create_blog_post/', views.create_blog_post, name="create_blog_post"),
]
