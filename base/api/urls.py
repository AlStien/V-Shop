from django.urls import path

from base.api.serializers import LoginUserSerializer

from . import views

app_name = 'base-api'
urlpatterns = [
    path('Account/', views.AccountList.as_view(), name="AccountList"),
    path('Account/<int:pk>', views.AccountDetails.as_view(), name="AccountDetail"),
    path('Account/create-account/', views.AccountList.as_view(), name="create-account"),
    path('Account/otp/verify/', views.OTPView.as_view(), name="verify-otp"),
    path('Account/login/', views.LoginAPIView.as_view(), name="login")
]