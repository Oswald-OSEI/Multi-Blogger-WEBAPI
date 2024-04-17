from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BlogHandleSerializer
from .models import BlogHandle
from blogapp.models import Blog
from blogapp.serializers import BlogSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@api_view(['POST'])
#this function carries out bloghandle creation
def create_handle(request):
    if request.method== 'POST':
        handle = BlogHandleSerializer(data = request.data)
        handle['blogger'] = request.user
        if handle.is_valid(raise_exception = True):
            handle.blogger.isBlogger=True
            handle.save()

#this function serves as a return reverse handle that introduces the blogger to his created blog handle
@api_view(['GET'])
def myhandle(request, handle_slug):
    handle = BlogHandle.objects.all().filter(slug=handle_slug, blogger__id=request.user)
    return Response('welcome to {handle.Blogger.first_name}')

#this function carries out update on handle details
@api_view(['POST'])
def updateHandle(request, handle_name):
    try:
        blog = BlogHandle.Objects.get(slug=handle_name, blogger = request.user)
        updated_blog = BlogSerializer(blog, data = request.data)
        if updated_blog.is_valid(raise_exception = True):
            updated_blog.save()
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
        bloghandle = BlogHandle.objects.all().filter(slug=handle_slug, blogger = request.user)
        if request.method == 'POST':
            blog = BlogSerializer(data = request.data)
            blog['blog_handle'] = bloghandle
            if blog.is_valid(raise_exception = True):
                blog.save()
    except ObjectDoesNotExist:
        return Response("You are not authorised to add blogs on this blog")

#this function updates a blog
@api_view(['GET', 'POST'])
def updateBlog(request, handle_name,blog_slug):
    try:
        blog = Blog.objects.get(handle__slug=handle_name, blog_slug=slug, handle__blogger=request.user)
        updated_blog = BlogSerializer(blog, data = request.data)
        if updated_blog.is_valid(raise_exception = True):
            updated_blog.save()
        else:
            return Response("Update not saved")
    except ObjectDoesNotExist:
        return Response('Blog does not exist')

#this function deletes a blog
@api_view(['GET', 'POST'])
def deleteblog(request, handle_name, blog_slug):
    try:
        blog = Blog.objects.all().filter(blog_slug=blog_slug, handle__slug = handle_name, handle__blogger = request.user)
        blog.delete()
    except ObjectDoesNotExist:
        return Response("You are don't have this permission")