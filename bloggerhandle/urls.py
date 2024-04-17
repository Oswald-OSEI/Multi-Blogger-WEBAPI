from django.urls import path
from .import views

urlpatterns = [
    path("CreateHandle/", views.create_handle, name = "createbloghandle"), 
    path("<slug:handle_slug>/", views.myhandle, name = "myhandle"), 
    path("<slug:handle_name>/updatehandle/", views.updateHandle, name = "updatehandle"), 
    path("<slug:handle_slug>/allblogs/", views.myblogs, name = "myBlogs"), 
    path("<slug:handle_slug>/createblog/", views.addblog, name = "newblog"), 
    path("<slug:handle_name>/<slug:blog_slug>/updateblog/", views.updateBlog, name = "blogupdate"), 
    path("<slug:handle_name>/<slug:blog_slug>/deleteblog/",views.deleteblog, name = "delete"),
]