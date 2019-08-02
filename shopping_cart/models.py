from __future__ import unicode_literals

from django.db import models

from products.models import Product
from accounts.models import Profile

# Create your models here.
class Orderitem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True, related_name='orderitems')
    is_ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.title

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    items = models.ManyToManyField(Orderitem, related_name='order_item')
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='orders', null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)
