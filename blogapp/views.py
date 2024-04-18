from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Blog, BlogReview
from .serializers import BlogSerializer, BlogReviewSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#a register who has signed in can read blog via this function
@api_view(['GET'])
def readBlog(request, blog_slug):
    try:
        blog = BlogSerializer(Blog.objects.get(slug=blog_slug)).data
        reviews = BlogReview.objects.all().filter(blog=blog)
        review_data = BlogReviewSerializer(reviews, many=True).data
        context={
            'blog':blog,
            'review_data':review_data
        }
        return Response(context)
    
    except ObjectDoesNotExist:
        return Response('blog does not exist')
#blog allows reader to write review on the blog
@api_view(['POST'])
def writeReview(request, blog_slug):
    if request.method == 'POST':
        review = BlogReviewSerializer(data = request.data)
        if Blog.handle.blogger == request.user:
            return Response('sorry, your review cannot be registered')
        else: 
            if review.is_valid(raise_expection = True):
                cd = review.data
                written_review = BlogReview.objects.create(
                    content = cd.get('content'),
                    rating = cd.get("rating"), 
                    reviewer = request.user
                )
                written_review.save()
            else:
                return Response('rewrite review')

#blog allows reader to read all othr comments on a blog
@api_view(['GET'])
def viewReviews(request, blog_slug):
    reviews = BlogReview.objects.all().filter( blog__slug = 'blog_slug')
    review_data = BlogReviewSerializer(reviews, many=True).data
    return Response(review_data)

#gives a reader the chance to view list of all blogs from a particular blogger
@api_view(['GET'])
def viewHandleBlogs(request, handle_slug):
    blogs = Blog.objects.all().filter(handle__slug = handle_slug)
    blogs = BlogSerializer(blogs, many=True).data
    return Response(blogs)

