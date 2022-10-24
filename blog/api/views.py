from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics,status
from blog.api.pagination import CustomLimitOffsetPagination
from blog.api.permissions import IsAdminUserOrReadOnly, IsPostOwnerOrReadOnly
from rest_framework.pagination import CursorPagination
from blog.api.serializers import (
    BlogPostSerializer, 
    CategorySerializer, 
    LikeSerializer,
    CommentSerializer
    )
from blog.models import (
    BlogPost, 
    Category, 
    Like,
    PostView,
    Comment
    )


class CursorSetPagination(CursorPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    ordering = 'id'  # '-created' is default

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BlogPostView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status="p")
    serializer_class = BlogPostSerializer
    pagination_class = CursorSetPagination
    

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # PostView.objects.get_or_create(user=request.user, post=instance)
        PostView.objects.create(user=request.user, post=instance)
        return Response(serializer.data)

class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(BlogPost, slug=slug)
        user = self.request.user
        comments = Comment.objects.filter(post=blog, user=user)
        if comments.exists():
            raise ValidationError(
                "You can not add another comment, for this Post !")
        serializer.save(post=blog, user=user)

# class LikeView(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        print(request.data.get("user"))
        user = request.data.get('user')
        post = request.data.get('post')
        serializer = self.get_serializer(data=request.data)
        exists_like = Like.objects.filter(user=user, post=post)
        serializer.is_valid(raise_exception=True)
        if exists_like:
            exists_like.delete()
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

