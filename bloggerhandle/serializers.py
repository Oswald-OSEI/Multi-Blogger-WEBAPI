from rest_framework import serializers
from .models import BlogHandle

class BlogHandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogHandle
        fields = ['handle_name', 'banner']
