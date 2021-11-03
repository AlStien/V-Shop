from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import EmailMultiAlternatives, message
from django.shortcuts import redirect
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from base.models import NewUser, OTP
from .serializers import AccountSerializer, CheckVerify, LoginUserSerializer
from VShop.settings import EMAIL_HOST_USER
import random
import datetime

# generating 4-digit OTP
otp = random.randint(1000, 9999)
# send otp to required email
def send_otp(email):
    OTP.objects.filter(otpEmail__iexact = email).delete()

    from_email, to = EMAIL_HOST_USER, email
    subject = "OTP for V-Shop Sign-Up"
    text_content = f'Your One Time Password for signing up on V-Shop is {otp}.\nValid for only 3 minutes.\nDO NOT SHARE IT WITH ANYBODY.'
    html_content = f'<span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px;"><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY.</p><p>Valid for only 5 minutes.</p><p>Your One Time Password for signing up on V-Shop is <strong style="font-size: 18px;">{otp}</strong>.</p></span>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    OTP.objects.create(otp = otp, otpEmail = email, time_created = timezone.now())

class AccountList(APIView):
    # get all account details 
    def get(self, request, format = None):
        users = NewUser.objects.all()
        serializer = AccountSerializer(users, many = True)
        serializer2 = CheckVerify(users, many = True)
        Serializer_list = [serializer.data, serializer2.data]

        content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK, 
            'data': Serializer_list,
        }
        return Response(content)

    # create a new account
    def post(self, request, format = None):
        serializer = AccountSerializer(data=request.data)
        user_email = request.data.get("email",)
        # checking if user already exists
        if NewUser.objects.filter(email = user_email).exists():
            message = {'message':'User already exists. Please Log-In'}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        else:
            if serializer.is_valid():
                send_otp(user_email)
                serializer.save()
            return Response(serializer.data)

class AccountDetails(APIView):
    # get a specific account details
    def get(self, request, pk, format = None):
        pk = int(pk)
        user = NewUser.objects.get(id=pk)
        serializer = AccountSerializer(user, many = False)
        return Response(serializer.data)

    # update a specific account details
    def put(self, request, pk, format = None):
        email = request.data.get("email",)
        user = NewUser.objects.get(email = email)
        serializer = AccountSerializer(instance=user, data = request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    # delete an account
    def delete(self, request, format = None):
        email = request.data.get("email",)
        user = NewUser.objects.get(email = email)
        user.update(is_active = False)
        return Response(status=status.HTTP_204_NO_CONTENT)

class OTPView(APIView):

    def post(self, request, format = None):
        data_otp = request.data.get("otp",)
        current_time = timezone.now()
        # print(otp)
        if str(data_otp) == str(otp):
            otp_obj = OTP.objects.get(otp=otp)
            user = NewUser.objects.filter(email = otp_obj.otpEmail)
            if otp_obj.time_created + datetime.timedelta(minutes=3) > current_time:
                # OTP verified
                user.update(is_verified = True)
                user.update(is_active = True)
                message = {'message':'OTP verified'}
                return Response(message,status=status.HTTP_202_ACCEPTED)
            # OTP expired
            message = {'message':'OTP expired'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        # OTP doesn't match
        message = {'message':'OTP doesn\'t match'}
        return Response(message,status=status.HTTP_401_UNAUTHORIZED)

class LoginAPIView(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        email = request.data.get("email",)
        password = request.data.get("password",)
        try:
            entered_usr = NewUser.objects.get(email__iexact=email)
            if check_password(password,entered_usr.password ):
                if not entered_usr.is_verified:
                    message = {'message':'Email address not verified by otp. Please Verify.'}
                    send_otp(email)
                    return Response(message, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    message = {'message':'Login verified'}
                    return Response(message, status=status.HTTP_202_ACCEPTED)
            else:
                message = {'message':'Incorrect password'}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        # check_pswd returns True for match

class ForgetResetPasswordView(APIView):

    def post(self, request):
        email = request.data.get("email",)
        try:
            entered_usr = NewUser.objects.get(email__iexact=email)
            send_otp(entered_usr)
            message = {'message':'OTP sent to registered Email'}
            return Response(message, status=status.HTTP_202_ACCEPTED)
        except:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
