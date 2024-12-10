from django.db import models
from django.db.models.signals import post_save
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.name