from django.urls import path

from . import views

urlpatterns = [
    path('', views.AccountList.as_view(), name="AccountList"),
    path('details/', views.AccountDetails.as_view(), name="AccountDetail"),
    path('update-account/', views.AccountDetails.as_view(), name="update-account"),
    path('create-account/', views.AccountList.as_view(), name="create-account"),
    path('delete-account/', views.AccountDetails.as_view(), name="delete-account"),
    path('otp/verify/', views.OTPView.as_view(), name="verify-otp"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('email-verify/', views.EmailVerifyView.as_view(), name="email-verify"),
    path('reset-password/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
]