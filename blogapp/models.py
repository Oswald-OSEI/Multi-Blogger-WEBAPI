from django.db import models
from accounts.models import Account
from django.utils.text import slugify 
from bloggerhandle.models import BlogHandle


def user_blog_images(instance, filename):
    return 'user_{0}/blogs/{1}/{2}/{3}'.format(instance.handle.blogger.email, instance.handle.handle_name, instance.Title, filename)

class Blog(models.Model):
    handle = models.ForeignKey(BlogHandle, on_delete = models.CASCADE, blank = True)
    Title = models.CharField(max_length = 100, unique=True)
    Content = models.TextField()
    blog_slug = models.SlugField(unique = True, blank = True)
    Pictures = models.ImageField(upload_to=user_blog_images)
    Date_Uploaded = models.DateTimeField(auto_now_add=True)
    last_Updated = models.DateTimeField(auto_now=True)

class BlogReview(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE, null = True)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
            