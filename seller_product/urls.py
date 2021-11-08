from django.urls import path

from . import views

urlpatterns = [
    path('add-product/', views.Product_create_api.as_view()),
    path('add-comment/', views.Comment_add_api.as_view()),

]