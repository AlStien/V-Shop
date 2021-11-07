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
        try:
            # getting the entered email user
            seller_email_instance = NewUser.objects.get(email=seller_email)
        except:
            return Response(data = {'message':'user with entered email not found'},status=status.HTTP_401_UNAUTHORIZED)
        # getting id for foreign key seller_email in Product model
        seller_id = seller_email_instance.id

        data = request.data
        # overrding post request data with seller_id
        data['seller_email'] = seller_id
        serializer = ProductSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(data = {'message': 'product saved sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(data = {'message': 'Invalid data entered'},status=status.HTTP_401_UNAUTHORIZED)
