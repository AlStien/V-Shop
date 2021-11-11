from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductView.as_view()),
    path('add-product/', views.ProductView.as_view()),
    path('add-comment/', views.Comment_add_api.as_view()),
    path('wishlist/', views.WishlistView.as_view())

]