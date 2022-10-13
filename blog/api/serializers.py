from rest_framework import serializers
from blog.models import BlogPost, Category, Comment, Like, Post_view


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    post_view_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "title",
            "author",
            "category_id",
            "category",
            "content",
            "image",
            "published_date",
            "last_updated_date",
            "status",
            "like_count",
            "comment_count",
            "post_view_count",
        )
        read_only_fields = (
            "published_date",
            "updated_date",
        )

    def get_like_count(self,obj):
        return Like.objects.filter(post=obj.id).count()

    def get_comment_count(self,obj):
        return Comment.objects.filter(post=obj.id).count()

    def get_post_view_count(self,obj):
        return Post_view.objects.filter(post=obj.id).count()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField()
    post = serializers.StringRelatedField()
    post_id = serializers.IntegerField()
    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = "__all__"