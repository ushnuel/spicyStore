from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from django.urls import reverse
from category.models import Category

from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    slug = models.SlugField(allow_unicode=True, unique=True)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images/%Y/%m/%d')


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'username':self.user.username, 'pk':self.pk, 'slug':self.slug})


    class Meta:
        ordering = ['-created_at']
