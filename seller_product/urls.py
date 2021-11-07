from django.urls import path

from . import views

urlpatterns = [
    path('', views.Product_create_api.as_view()),
]