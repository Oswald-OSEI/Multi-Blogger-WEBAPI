from rest_framework import serializers
from .models import Blog, BlogHandle, BlogReview

class BlogReviewSerializer:
    class Meta:
        model = BlogReview
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['Title', 'Content', 'Pictures']
        
