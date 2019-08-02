import random
import datetime
import string
from datetime import date

from shopping_cart.models import Orderitem

def SaveOrderItem(order):
    order_item = Orderitem.objects.filter(order=order)
    order_item.save()
    return order_item

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str
