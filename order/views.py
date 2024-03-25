import json
import uuid
from django.db.models.query import QuerySet
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutForm
from cart.carts import Cart, Coupon
from product.models import Product
from .models import Order, OrderItem

# Create your views here.


class Checkout(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'order/checkout.html', context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)

        if form.is_valid():
            data = form.cleaned_data
            print(data)
            return JsonResponse({
                'success': True,
                'errors': None,
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors),
            })


class SaveOrder(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, *args, **kwargs):
        customer_info = json.loads(self.request.body)
        user_cart = Cart(self.request).cart
        cart = Cart(self.request)
        coupon_id = cart.coupon
        products = Product.objects.filter(id__in=list(user_cart.keys()))
        ordered_products = []

        for product in products:
            order_item = OrderItem.objects.create(
                product=product,
                price=product.price,
                quantity=user_cart[str(product.id)]['quantity']
            )
            ordered_products.append(order_item)

        order = Order.objects.create(
            user=self.request.user,
            transaction_id=uuid.uuid4().hex,

            **customer_info
        )

        order.order_items.add(*ordered_products)

        if coupon_id:
            order.coupon = Coupon.objects.get(id=coupon_id)
            order.save()
            
        if float("%.2f" % cart.total()) != float(order.total):
            order.paid = False
            order.save()

        cart.clear()

        return JsonResponse({'success': True})


class Orders(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    model = Order
    template_name = 'order/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
