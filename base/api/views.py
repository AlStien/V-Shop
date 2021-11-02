import collections
from datetime import datetime
from VShop import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from base.models import NewUser as Entry, OTP
from .serializers import AccountSerializer, OtpSerializer, CheckVerify, LoginUserSerializer
from django.http import HttpResponse, response
from django.utils import timezone
import datetime
from .renderers import UserJSONRenderer
from base.models import NewUser
from django.contrib.auth.hashers import check_password
class AccountList(APIView):
    def get(self, request, format = None):
        notes = Entry.objects.all()
        serializer = AccountSerializer(notes, many = True)
        serializer2 = CheckVerify(notes, many = True)
        Serializer_list = [serializer.data, serializer2.data]

        content = {
            'status': 1, 
            'responseCode' : status.HTTP_200_OK, 
            'data': Serializer_list,
        }
        return Response(content)

    def post(self, request, format = None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class AccountDetails(APIView):
    def get(self, request, pk, format = None):
        pk = int(pk)
        notes = Entry.objects.get(id=pk)
        serializer = AccountSerializer(notes, many = False)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        pk = int(pk)
        note = Entry.objects.get(id = pk)
        serializer = AccountSerializer(instance=note, data = request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk, format = None):
        pk = int(pk)
        note = Entry.objects.get(id = pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

import random
from django.core.mail import send_mail

class OTPView(APIView):

    otp = random.randint(1000, 9999)
    # email = settings.EMAIL_HOST_USER
    def send_otp(email, otp=otp):
        # OTP.objects.filter(email__iexact = email).delete()
        print(email)
        send_mail(
            "OTP for V-Shop Sign-Up.", f'Your One Time Password for signing up on V-Shop is {otp}.\nValid for only 5 minutes.\nDO NOT SHARE IT WITH ANYBODY.', 'drugged.to.art@gmail.com', ['artistakshaybro22@gmail.com'], fail_silently=False
        )

        OTP.objects.create(otp = otp, email = email)
        
        return HttpResponse('otp')

    def post(self, request, otp=otp, format = None):
        data_otp = request.data.get("otp",)
        data_email = request.data.get("email",)
        # user = Entry.objects.get(email__iexact = data_email)
        current_time = timezone.now()
        print(data_otp)
        print(otp)
        if str(data_otp) == str(otp):
            otp_obj = OTP.objects.get(otp=otp)
            if otp_obj.time_created + datetime.timedelta(minutes=5) > current_time:
                # OTP verified
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
            # entered_usr = NewUser.objects.get(email=email)
            entered_usr = NewUser.objects.get(email__iexact=email)
        except:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        # entered_usr.password
        # print(email,password)

        # check_pswd returns True for match
        if check_password(password,entered_usr.password ):
            # print("akdfgkj")
            message = {'message':'Login verified'}
            return Response(message, status=status.HTTP_202_ACCEPTED)
        message = {'message':'Incorrect password'}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        # serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)

        # return Response(serializer.data, status=status.HTTP_200_OK)
