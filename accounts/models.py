from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
from .managers import manager


# Create your models here.
class Account(AbstractUser):
    username = None
    email = models.EmailField(null = True, unique = True)
    name = models.CharField(max_length = 200, null = True)
    last_name = models.CharField(max_length = 200, null = True)
    isBlogger = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = manager()

def user_profile_pics_directory(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profilepics/{1}'.format(instance.account_holder.email, filename)

class Profile(models.Model):
    account_holder = models.OneToOneField(Account, on_delete = models.CASCADE)
    profile_picture = models.ImageField(upload_to= user_profile_pics_directory, null = True)
    date_of_birth = models.DateField(null=True, blank=True)
    telephone_number= models.CharField(max_length = 10, null=True)
    about = models.TextField(null = True)
    gender_choices = (
        ("M", "MALE"), 
        ("F", "FEMALE"),
    )
    Gender = models.CharField(max_length = 1, choices = gender_choices, null = True)
    date_created = models.DateTimeField(auto_now_add = True)
    last_update = models.DateTimeField(auto_now = True)
