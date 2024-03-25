from django.conf import settings

from product.models import Product
from .models import Coupon


class Cart(object):
    def __init__(self, request) -> None:
        self.session = request.session
        self.cart_id = settings.CART_ID
        self.coupon_id = settings.COUPON_ID
        cart = self.session.get(self.cart_id)
        coupon = self.session.get(self.coupon_id)
        self.cart = self.session[self.cart_id] = cart if cart else {}
        self.coupon = self.session[self.coupon_id] = coupon if coupon else None

    def update(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        self.session[self.cart_id].setdefault(str(product_id), {"quantity": 0})
        updated_quantity = self.session[self.cart_id][str(
            product_id)]["quantity"] + quantity
        self.session[self.cart_id][str(
            product_id)]["quantity"] = updated_quantity
        self.session[self.cart_id][str(
            product_id)]["subtotal"] = updated_quantity * float(product.price)

        if updated_quantity < 1:
            del self.session[self.cart_id][str(product_id)]

        self.save()

    def add_coupon(self, coupon_id):
        self.session[self.coupon_id] = coupon_id
        self.save()

    def __iter__(self):
        products = Product.objects.filter(id__in=list(self.cart.keys()))
        cart = self.cart.copy()

        for item in products:
            product = Product.objects.get(id=item.id)
            cart[str(item.id)]['product'] = {
                "id": item.id,
                "title": item.title,
                "category": item.category.title,
                "price": float(item.price),
                "thumbnail": item.thumbnail,
                "slug": item.slug,
            }
            yield cart[str(item.id)]

    def save(self):
        self.session.modified = True

    def __len__(self):
        return len(list(self.cart.keys()))

    def clear(self):
        try:
            del self.session[self.cart_id]
            del self.session[self.coupon_id]
        except:
            pass
        self.save()

    def restore_after_logout(self, cart={}, coupon=None):
        self.cart = self.session[self.cart_id] = cart
        self.coupon = self.session[self.coupon_id] = coupon
        self.save()

    def total(self):
        amount = sum(product['subtotal'] for product in self.cart.values())

        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            amount -= amount*(coupon.discount/100)

        return amount
