from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from products.models import Product
from shopping_cart.models import Order, Orderitem
from shopping_cart.extras import generate_order_id
import datetime
from django.conf import settings
from shopping_cart.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.views.decorators.csrf import csrf_exempt
import random
import string


# Create your views here.
def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user) # get the current user
    order = Order.objects.filter(owner=user_profile, is_ordered=False) # get the order from the filtered user
    if order.exists():
        return order[0] # get the only order from the filtered orders
    return 0

@login_required
def add_to_cart(request, **kwargs):
    user_profile = Profile.objects.get_or_create(user=request.user) # get the user profile
    product = Product.objects.filter(id=kwargs.get('item_id',"")).first() # filter products to add by id

    if product in request.user.user_profile.goods.all(): # check if user already owns the product
        messages.info(request, 'This product is already added')
        return redirect(reverse('products:all'))

    order_item, status = Orderitem.objects.get_or_create(product=product) #create order item of the selected product

    user_order, status = Order.objects.get_or_create( owner=request.user.user_profile,
                                                    is_ordered=False ) #create order associated with the user

    user_order.items.add(order_item)
    if not status:
        user_order.ref_code = generate_order_id() # generate a reference code
        user_order.save()

    messages.info(request, 'item successfully added to cart')
    return redirect(reverse('products:all'))

@login_required
def delete_from_cart(request, item_id):
    item_to_delete = Orderitem.objects.filter(id=item_id) # get item to delete from orderitem

    if item_to_delete.exists(): #check if item exists
        item_to_delete[0].delete()
        messages.info(request, 'Item has been deleted from cart')
    return redirect(reverse('shopping_cart:order_summary'))

@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order':existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)

@login_required
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {
        'order':existing_order
    }
    return render(request, 'shopping_cart/checkout.html', context)

@login_required
def paystack_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.user_profile)

    email = request.user.email
    amount = order.get_cart_total() * 100
    ref = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])
    callback_url = 'https://kemspicy.com/shopping_cart/success/?order_id=' + str(order_id)

    response = initialize_paystack(email, amount, ref, callback_url)
    checkout_url = response['data']['authorization_url']
    if checkout_url:
        return redirect(checkout_url)

    return HttpResponse(status=404)

@login_required
def flutter_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.user_profile)
    email = request.user.email
    amount = order.get_cart_total()
    currency = 'NGN'
    redirect_url = 'https://kemspicy.com/shopping_cart/success/?order_id=' + str(order_id)
    txref = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(18)])

    feedback = flutter_initialize(email, amount, txref, redirect_url, currency)
    payment_url = feedback['data']['link']
    if payment_url:
        return redirect(payment_url)

    return HttpResponse(status=404)

def flutter_initialize(email, amount, txref, redirect_url, currency):
    data = {
        'txref': txref,
        'customer_email': email,
        'amount': amount,
        'currency': currency,
        'PBFPubKey': settings.FLUTTER_PUBLIC_KEY,
        'redirect_url': redirect_url,
    }
    headers = {
        'content-type':'application/json'
    }
    return requests.post(url='https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/hosted/pay',
        data=data).json()

def initialize_paystack(email, amount, ref, callback_url):
    data = {
        "reference": ref,
        "amount": amount,
        "email": email,
        "callback_url": callback_url
    }

    return requests.post(url='https://api.paystack.co/transaction/initialize',
    headers=settings.HEADER, data=data).json()

@login_required
def update_transaction_records(request, order_id, **kwargs):
    order_to_purchase = Order.objects.filter(id=order_id).first() # get the order being processed

    #update the order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    order_items = order_to_purchase.items.all() # get all the items in the order
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now()) # update the order
    user_profile = get_object_or_404(Profile, user=request.user) # get the user profile
    order_products = [item.product for item in order_items]
    element = order_products[0] # get the products from the items

    user_profile.goods.add(element)  # add the products to the user's goods
    user_profile.save()

    return redirect(reverse('accounts:my_profile'))

@login_required
def delete_order(request, order_id):
    order_to_delete = Order.objects.filter(id=order_id, is_ordered=True).first() # get the order to delete
    user_profile = get_object_or_404(Profile, user=request.user) # get the current user

    all_items = order_to_delete.items.all() # get the items in the order
    products = [item.product for item in all_items] # get the products from the order items
    product = products[0]

    user_profile.goods.remove(product)

    if order_to_delete:
        order_to_delete.delete()

    messages.info(request, 'Order has been deleted')
    return redirect(reverse('accounts:my_profile'))

@csrf_exempt
def success(request):
    id = request.GET.get('order_id', '')
    order = Order.objects.filter(id=id).first()

    return render(request, 'shopping_cart/success.html', {'order':order})
