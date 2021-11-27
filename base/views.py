# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# ------ For Sending E-Mail -------
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from VShop.settings import EMAIL_HOST_USER
# ------ Imports for User Views -------
from base.models import NewUser, OTP
from .serializers import (
    AccountSerializer,
    CheckVerify,
    LoginUserSerializer,
    ProfileSerializer,
    OTPSerializer,
)
# ------ Utilities -------
import random, datetime
from django.utils import timezone

# ------ For Sending OTP to passed E-Mail -------
def send_otp(email):
    # generating 4-digit OTP
    otp = random.randint(1000, 9999)
    if OTP.objects.filter(otp = otp).exists():
        if(otp > 9000):
            otp = random.randint(1000, otp)
        else:
            otp = random.randint(otp, 9999)
    OTP.objects.filter(otpEmail__iexact = email).delete()
    print(otp)

    from_email, to = EMAIL_HOST_USER, email
    subject = "OTP for V-Shop Sign-Up"
    text_content = f'Your One Time Password for signing up on V-Shop is {otp}.\nValid for only 3 minutes.\nDO NOT SHARE IT WITH ANYBODY.'
    html_content = f'<span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px;"><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY.</p><p>Valid for only 5 minutes.</p><p>Your One Time Password for signing up on V-Shop is <strong style="font-size: 18px;">{otp}</strong>.</p></span>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    OTP.objects.create(otp = otp, otpEmail = email, time_created = timezone.now())

# ------ To Get List of All Accounts -------
class AccountList(APIView):
    permission_classes = (AllowAny,)
    
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
        if NewUser.objects.filter(email__iexact = user_email).exists():
            message = {'message':'User already exists. Please Log-In'}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        else:
            # for validation of password (default and custom)
            # validate_password throws exception for valdation errors
            try:
                validate_password(request.data.get('password',))
                if serializer.is_valid():
                    send_otp(user_email)
                    serializer.save()
                return Response(serializer.data)
            except:
                return Response({'message': 'Please Enter a valid password. Password should have atleast 1 Capital Letter, 1 Number and 1 Special Character in it.'},status=status.HTTP_400_BAD_REQUEST)

# ------ User Profile -------
class AccountDetails(APIView):
    # get a specific account details
    def get(self, request, format = None):
        user = NewUser.objects.get(email = request.user.email)
        # user = NewUser.objects.get(id=pk)
        serializer = ProfileSerializer(user, many = False)
        return Response(serializer.data)

    # update a specific account details
    def put(self, request, format = None):
        serializer = ProfileSerializer(instance=request.user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({'message':'Invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    # delete an account
    def delete(self, request, format = None):
        email = request.user.email
        user = NewUser.objects.get(email = email)
        user.delete()
        return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

# ------ To Verify OTP -------
class OTPView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        data = OTP.objects.all()
        return Response(OTPSerializer(data, many=True).data)

    def post(self, request, format = None):
        data_otp = request.data.get("otp",)
        data_email = request.data.get("email",)
        user = OTP.objects.get(otpEmail__iexact = data_email)
        current_time = timezone.now()
        print(current_time)
        print(user.time_created)
        # OTP expired
        if user.time_created + datetime.timedelta(minutes=3) < current_time:
            message = {'message':'OTP expired'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        else:
            if OTP.objects.filter(otp = data_otp).exists() and (OTP.objects.get(otp = data_otp) == OTP.objects.get(otpEmail = data_email)):
                otp_obj = OTP.objects.get(otp = data_otp)
                print(otp_obj)
                print(data_otp)
                user = NewUser.objects.filter(email__iexact = otp_obj.otpEmail)
                if otp_obj.time_created + datetime.timedelta(minutes=3) > current_time:
                    # OTP verified
                    user.update(is_verified = True)
                    user.update(is_active = True)
                    message = {'message':'User verified'}
                    return Response(message,status=status.HTTP_202_ACCEPTED)
                # OTP expired
                message = {'message':'OTP expired'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
            # OTP doesn't match
            else:
                message = {'message':'OTP doesn\'t match'}
                return Response(message,status=status.HTTP_401_UNAUTHORIZED)

# ------ Login -------
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    serializer_class = LoginUserSerializer

    def post(self, request):
        email = (request.data.get("email",))
        email = email.lower()
        password = request.data.get("password",)
        try:
            entered_usr = NewUser.objects.get(email__iexact=email)
            if check_password(password,entered_usr.password ):
                if not entered_usr.is_verified:
                    message = {'message':'Email address not verified by otp. Please Verify.'}
                    send_otp(email)
                    return Response(message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
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

# ------ To Verify Email and Send OTP to it -------
class EmailVerifyView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format = None):
        email = request.data.get("email")
        if NewUser.objects.filter(email__iexact = email).exists():
            user = NewUser.objects.get(email__iexact = email)
            seraializer = CheckVerify(user)
            return Response(seraializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
            

    def post(self, request):
        email = request.data.get("email",).lower()
        if NewUser.objects.filter(email = email).exists():
            send_otp(email)
            message = {'message':'OTP sent to registered Email'}
            return Response(message, status=status.HTTP_202_ACCEPTED)
        else:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

# ------ Password Reset -------
class PasswordChangeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email",)
        password = request.data.get("new password")
        if OTP.objects.filter(otpEmail__iexact = email).exists():
            if NewUser.objects.filter(email__iexact = email).exists():
                user = NewUser.objects.get(email__iexact = email)
                if user.password == password:
                    message = {'message':'Password cannot be same as old one'}
                    return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    validate_password(password)
                    user.password = make_password(password)
                    user.save()
                    message = {'message':'Password Changed Successfully'}
                    return Response(message, status=status.HTTP_202_ACCEPTED)
            message = {'message':'Email doesn\'t exist'}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
            
        else:
            message = {'message':'Email entered does not match the verified Email.'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)


    permission_classes = [IsAuthenticated,]
    def put(self, request, format=None):
        
        email = request.user.email

        if OTP.objects.filter(otpEmail__iexact = email).exists():
            if NewUser.objects.filter(email__iexact = email).exists():
                user = NewUser.objects.get(email__iexact = request.user.email)
                user.is_seller = True
                user.save()
                serializer = ProfileSerializer(user, many=False)
                return Response(serializer.data)  
        return Response(message = {'message':'incorrect credentials'}, status=status.HTTP_204_NO_CONTENT)  

# ------ Prime Membership -------
class PrimeMember(APIView):

    permission_classes = [IsAuthenticated,]
    def put(self, request, format=None):
        
        email = request.user.email

        if OTP.objects.filter(otpEmail__iexact = email).exists():
            if NewUser.objects.filter(email__iexact = email).exists():
                user = NewUser.objects.get(email__iexact = request.user.email)
                user.is_prime = True
                user.save()
                serializer = ProfileSerializer(user, many=False)
                return Response(serializer.data)  
        return Response(message = {'message':'incorrect credentials'}, status=status.HTTP_204_NO_CONTENT)  
