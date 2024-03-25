from .carts import Cart


def cart(request):
    cart = Cart(request)
    
    if len(list(cart.cart.keys())) <1:
        try:
            del cart.session[cart.coupon_id]
        except:
            ...
    return {"cart": Cart(request)}
