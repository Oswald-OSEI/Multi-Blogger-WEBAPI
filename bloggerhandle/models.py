from django.db import models
from accounts.models import Account
from django.utils.text import slugify

# Create your models here.
def user_bloghandle_banner(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/bloghandlebanner/{1}'.format(instance.blogger.email, filename)

class BlogHandle(models.Model):
    handle_name = models.CharField(max_length = 150, unique = True)
    slug = models.SlugField( unique = True )
    blogger = models.OneToOneField(Account, on_delete = models.CASCADE, blank=True)
    banner = models.ImageField(upload_to=user_bloghandle_banner)

    def generate_slug(self, args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.handle_name)
            super().save(*args, **kwargs)