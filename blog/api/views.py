from rest_framework import viewsets
from blog.api.serializers import BlogPostSerializer, CategorySerializer

from blog.models import BlogPost, Category


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BlogPostView(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer