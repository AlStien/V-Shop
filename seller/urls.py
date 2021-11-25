from django.urls import path

from . import views

urlpatterns = [
    path('sellers/', views.SellerListView.as_view(), name="sellers"),
    path('become-seller/', views.BecomeSellerView.as_view(), name="become-seller"),
    path('seller-dashboard/', views.SellerProductsView.as_view()),
]