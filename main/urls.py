from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('blog_post/<int:pk>/', views.blog_post, name="blog_post"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:category>/', views.category, name="category"),
]
