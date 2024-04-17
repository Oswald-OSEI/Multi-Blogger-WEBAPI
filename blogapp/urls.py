from django.urls import path
from .import views

urlpatterns = [
    path('<slug:blog_slug>/readblog/', views.readBlog, name = 'readblog'),
    path('<slug:blog_slug>/reviewblog/', views.writeReview, name = "ReviewBlog" ),
    path("<slug:blog_slug>/comments", views.viewReviews, name = "blogcomments"),
]