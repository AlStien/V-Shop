from django.urls import path
from rest_framework import request

from . import views

urlpatterns = [
    path('', views.ProductsView.as_view()),
    path('product-details/', views.ProductDetailsView.as_view()),
    # path('add-product/images/', views.ProductImageView.as_view()),
    path('add-product/', views.ProductView.as_view()),
    path('update-product/', views.ProductView.as_view()),
    path('add-comment/', views.Comment_add_api.as_view()),
    path('add-tag/', views.Tag_add_api.as_view()),
    path('wishlist/', views.WishlistView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('cart/add-product/', views.CartView.as_view()),
    path('cart/remove-product/', views.CartView.as_view()),
    path('cart/delete-product/', views.CartDeleteView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/checkout/', views.OrderView.as_view()),
    path('checkout-transaction/', views.CheckoutTransaction.as_view()),
    path('send-coupon/', views.SendCoupon.as_view()),
    path('search-product/', views.SearchProduct.as_view()),
    path('search-filter-product/', views.SearchFilterProduct.as_view()),
    path('view-comment/', views.Comment_view_api.as_view()),
    path('show-brands/', views.ShowBrands.as_view()),

]
