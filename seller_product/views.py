from django.http.response import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from seller_product.models import Product

from seller_product.serializers import ProductSerializer

from base.models import NewUser

class Product_create_api(APIView):
    def post(self, request, format=None):
        seller_email = request.data.get('seller_email',)
        seller_email_instance = NewUser.objects.get(email=seller_email)

        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(email=seller_email_instance)
            # serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return HttpResponse(str(seller_email_instance.email))
        
        # seller_email = request.data.get('seller_email',)
        # seller_email_instance = NewUser.objects.get(email=seller_email)
        
