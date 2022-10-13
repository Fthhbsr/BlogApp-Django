from .views import (
    CategoryView,
    BlogPostView
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('category', CategoryView)
router.register('post', BlogPostView)


urlpatterns = [

] + router.urls