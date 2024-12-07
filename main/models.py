from django.db import models
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class BlogPost(models.Model):
    heading = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.today())
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    