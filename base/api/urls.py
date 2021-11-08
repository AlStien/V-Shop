from os import name
from django.urls import path

from base.api.serializers import LoginUserSerializer

from . import views

app_name = 'base-api'
urlpatterns = [
    path('', views.AccountList.as_view(), name="AccountList"),
    path('detail/', views.AccountDetails.as_view(), name="AccountDetail"),
    path('create-account/', views.AccountList.as_view(), name="create-account"),
    path('otp/verify/', views.OTPView.as_view(), name="verify-otp"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('reset-password/email-verify/', views.EmailVerifyView.as_view(), name="email-verify"),
    path('reset-password/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
]