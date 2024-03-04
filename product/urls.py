from django.urls import path
from .views import (
    Home,
    ProductDetails,
    CategorDetails,
    ProductList,
    SearchProducts,
)

urlpatterns = [
    path('', Home.as_view(), name='home' ),
    path('product-details/<str:slug>/', ProductDetails.as_view(), name='product-details'),
    path('category-details/<str:slug>/', CategorDetails.as_view(), name='category-details'),
    path('product-list/', ProductList.as_view(), name='product-list'),
    path('search-products/', SearchProducts.as_view(), name='search-products'),
    
    
]
 