from .models import Order
from products.models import Product

def add_variable_to_context(request):

    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(is_ordered=False, owner=request.user.user_profile)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
            length = len(current_order_products)

            context = {
                    'length': length,
                    }

            return context
    return {}
