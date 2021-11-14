from django.urls import path
from rest_framework import request

from . import views

urlpatterns = [
    path('', views.ProductsView.as_view()),
    path('add-product/', views.ProductView.as_view()),
    path('add-comment/', views.Comment_add_api.as_view()),
    path('add-tag/', views.Tag_add_api.as_view()),
    path('wishlist/', views.WishlistView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('cart/add-product/', views.CartView.as_view()),
    path('cart/delete-product/', views.CartView.as_view()),
    path('search-product/', views.SearchProduct)
    # path('view-my-products/',views.Product_view_seller_api.as_view()),
]