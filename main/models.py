from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heading = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default="", blank=True, null=True)
    image = models.ImageField(upload_to="images/post_image")
    date = models.DateField(default=datetime.datetime.today)
    likes = models.ManyToManyField(User, related_name="blog_posts")
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.heading

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(
        BlogPost, related_name="comments", on_delete=models.CASCADE
    )  # related_name to access comments via BlogPost class
    title = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog_post.heading} - {self.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/profile_p/", default='images/profile_p/default.png')
    biography = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name="followers", null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if not self.biography and self.user:
            self.biography = f"I am {self.user.username}"
        super().save(*args, **kwargs)

# Signal to create a Profile when a User is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Optional: Signal to save Profile when User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()