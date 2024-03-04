from django.urls import path
from .views import AddToCart, CartItems

urlpatterns = [
    path("add-to-cart/<int:product_id>/",
         AddToCart.as_view(), name='add-to-cart'),
    path('cart/', CartItems.as_view(), name='cart'),
]
