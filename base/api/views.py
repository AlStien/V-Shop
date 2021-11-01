import collections
from VShop import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from base.models import NewUser as Entry, OTP
from .serializers import AccountSerializer, OtpSerializer, CheckVerify
from django.http import HttpResponse, response

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

        send_mail(
            "OTP for V-Shop Sign-Up.", f'Your One Time Password for signing up on V-Shop is {otp}. DO NOT SHARE IT WITH ANYBODY.', 'drugged.to.art@gmail.com', ['Ayush2010051@akgec.ac.in'], fail_silently=False
        )

        OTP.objects.create(otp = otp, email = email)
        
        return HttpResponse('otp')

    def post(self, request, otp=otp, format = None):
        data_otp = request.data.get("otp",)
        data_email = request.data.get("email",)
        # user = Entry.objects.get(email__iexact = data_email)
        if str(data_otp) == str(otp):
            return HttpResponse("GG")
        return HttpResponse("NT")