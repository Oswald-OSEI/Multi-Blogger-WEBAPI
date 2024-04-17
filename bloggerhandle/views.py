from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BlogHandleSerializer
from .models import BlogHandle
from accounts.models import Account
from blogapp.models import Blog
from blogapp.serializers import BlogSerializer
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@api_view(['POST'])
#this function carries out bloghandle creation
def create_handle(request):
    if request.method== 'POST':
        handle = BlogHandleSerializer(data = request.data)
        if handle.is_valid(raise_exception = True):
            cd = handle.data
            create_handler = BlogHandle.objects.create(
                blogger=request.user, 
                handle_name = cd.get('handle_name'), 
                banner = request.FILES.get('banner'),
                slug = slugify(cd.get('handle_name'))
            )
            create_handler.save()
            RegBlogger = Account.objects.get(id = create_handler.blogger.id)
            RegBlogger.isBlogger=True
            RegBlogger.save()
            return Response('succefully created your handle')

#this function serves as a return reverse handle that introduces the blogger to his created blog handle
@api_view(['GET'])
def myhandle(request, handle_slug):
    handle = BlogHandleSerializer(BlogHandle.objects.get(slug=handle_slug, blogger=request.user))
    return Response(handle.data)

#this function carries out update on handle details
@api_view(['POST'])
def updateHandle(request, handle_name):
    try:
        blog = BlogHandle.objects.get(slug=handle_name, blogger = request.user)
        updated_handle = BlogHandleSerializer(blog, data = request.data)
        if updated_handle.is_valid(raise_exception = True):
            banner_update = request.FILES.get('banner')
            if banner_update is not None:
                updated_handle.save(banner=banner_update)
            else:
                updated_handle.save()
            return Response(updated_handle.data)
        else:
            return Response("Update not saved")
    except ObjectDoesNotExist:
        return Response('Handle does not exist')

#this function retrieves all the blogs hosted by a bloghandle
@api_view(['GET'])   
def myblogs(request, handle_slug):
    try:
        blogs = (Blog.objects.all().filter(handle__slug=handle_slug, handle__blogger=request.user))
        blogs_data = BlogSerializer(blogs, many = True).data
        return Response(blogs_data)
    except ObjectDoesNotExist:
        return Response('You have no blogs')

#creates a new blog in a blog handle
@api_view(['POST'])
def addblog(request, handle_slug):
    try:
        bloghandle = BlogHandle.objects.get(slug=handle_slug, blogger = request.user)
        if request.method == 'POST':
            blog = BlogSerializer(data = request.data)
            if blog.is_valid(raise_exception = True):
                cd = blog.data
                creating_blog = Blog.objects.create(
                    handle = bloghandle, 
                    Title = cd.get('Title'), 
                    Content = cd.get('Content'), 
                    Pictures = request.FILES.get('Pictures'),
                    blog_slug = slugify(cd.get('Title'))  
                )
                creating_blog.save()
                return Response('Blog Uploaded')
    except ObjectDoesNotExist:
        return Response("You are not authorised to add blogs on this blog")

#this function updates a blog
@api_view(['POST'])
def updateBlog(request, handle_name,blog_slug):
    try:
        blog = Blog.objects.get(handle__slug=handle_name, blog_slug=blog_slug, handle__blogger=request.user)
        updated_blog = BlogSerializer(blog, data = request.data)
        if updated_blog.is_valid(raise_exception = True):
            if request.FILES.get('Pictures') is not None:
                Pics = request.FILES.get('Pictures')
                updated_blog.save(Pictures=Pics)
            else:
                updated_blog.save()
            return Response(updated_blog.data)
        else:
            return Response("Update not saved")
    except ObjectDoesNotExist:
        return Response('Blog does not exist')

#this function deletes a blog
@api_view(['POST'])
def deleteblog(request, handle_name, blog_slug):
    try:
        blog = Blog.objects.all().filter(blog_slug=blog_slug, handle__slug = handle_name, handle__blogger = request.user)
        blog.delete()
        return Response('Blog Deleted')
    except ObjectDoesNotExist:
        return Response("You are don't have this permission")