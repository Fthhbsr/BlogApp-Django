from django.urls import path
from .views import (
    BlogPostDetailView,
    CategoryView,
    BlogPostView,
    CommentView,
    LikeView
)
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('category', CategoryView)
# router.register('blog', BlogPostView)
# router.register('like', LikeView)


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('like/', LikeView.as_view()),
    path('posts/', BlogPostView.as_view()),
    path('posts/<str:slug>/', BlogPostDetailView.as_view()),
    path("posts/<str:slug>/add_comment/", CommentView.as_view()),

]
# urlpatterns += router.urls