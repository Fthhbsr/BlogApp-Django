from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from blog.models import BlogPost, Like
from .utils import get_random_code

@receiver(pre_save, sender=BlogPost)
def pre_save_create_slug(sender, instance,**kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + " " + get_random_code())

@receiver(pre_save, sender=Like)
def is_like_user(sender, instance,**kwargs):
    like = Like.objects.get(user=instance.user, post=instance.post)
    if like:
        like.delete()
    else:
        instance.save()