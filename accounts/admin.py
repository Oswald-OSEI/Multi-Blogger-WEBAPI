from django.contrib import admin
from .models import Account, Profile
from django.contrib.auth.admin import UserAdmin as baseAdmin
from blogapp.models import Blog, BlogReview
from bloggerhandle.models import BlogHandle
# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete= False

class BloggerHandle(admin.ModelAdmin):
    model = BlogHandle
    list_display = ('handle_name', 'blogger','slug',)
    readonly_fields = ('slug', 'blogger', )
    ordering = ('handle_name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(BlogHandle, BloggerHandle)


class BloggerReviewInline(admin.StackedInline):
    model = BlogReview
    can_delete = False

class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ('handle', 'Title', 'blog_slug', 'Date_Uploaded', 'last_Updated',)
    readonly_fields = ('handle', 'blog_slug', 'Date_Uploaded', 'last_Updated',)
    ordering = ('Date_Uploaded',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    inlines = (BloggerReviewInline, )
admin.site.register(Blog, BlogAdmin)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('account_holder','date_created', 'last_update')
    readonly_fields = ('account_holder', 'date_created', 'last_update', )
    ordering = ('date_created',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
   
admin.site.register(Profile, ProfileAdmin)  
  


class UserAccount(baseAdmin):
    model = Account
    list_display = ('email','first_name', 'last_name', 'last_login', 'is_active',)
    ordering = ("email",)
    readonly_fields = ('last_login',)
    filter_horizontal = ()
    list_filter = ("is_active", "is_staff",)
# makes password field readonly
    fieldsets = () 
    inlines = (UserProfileInline,)

admin.site.register(Account, UserAccount)
