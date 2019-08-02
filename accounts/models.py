from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.conf import settings
from django.db.models.signals import post_save
from products.models import Product

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='user_profile')
    goods = models.ManyToManyField(Product, blank=True, related_name='item')

    def __str__(self):
        return self.user.username

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=User)
