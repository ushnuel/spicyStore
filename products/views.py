from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

from django.http import Http404
from django.views import generic

from django.contrib.auth import get_user_model
User = get_user_model()

from . import models
from . import forms
from category.models import Category
from shopping_cart.models import Order

from django.db.models import Q

# Create your views here.

def Product_list(request):
    products = models.Product.objects.all()
    categories = Category.objects.all()

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(is_ordered=False, owner=request.user.user_profile)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

            context = {
                'products':products,
                'categories':categories,
                'current_order_products':current_order_products
            }

            return render(request, 'products/product-list.html', context)

    context = {
        'products':products,
        'categories':categories,
    }
    return render(request, 'products/product-list.html', context)

class ProductDetailView(generic.DetailView):
    model = models.Product
    template_name = 'products/product_detail.html'
    select_related = ('category')

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = models.Product.objects.filter(category__name=self.object.category.name).order_by('created_at')
        return context

class DeleteProduct(LoginRequiredMixin, generic.DeleteView):
    model = models.Product
    success_url = reverse_lazy('products:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__id = self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully')
        return super().delete(*args, **kwargs)

@login_required
def sell_product(request):
    if request.method == 'POST':
        form = forms.ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            #check if an image is provided
            if 'image' in request.FILES:
                product.ad_image = request.FILES['image']

            product.save()
            messages.info(request, 'Your product has been successfully submitted.')
            return redirect('products:create')
        else:
            messages.error(request, 'Invalid form, please fill the necessary fields')
            return redirect('products:create')
    else:
        form = forms.ProductCreateForm()
    return render(request, 'products/product_form.html', {'form': form })

def search_product(request):
    products = models.Product.objects.all()
    query = request.GET.get('search')

    results = products.filter(Q(title__icontains=query) | Q(price__icontains=query)).distinct()
    return render(request, 'products/search.html', {'results': results})
