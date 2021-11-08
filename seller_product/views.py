from django.http.response import HttpResponse
from rest_framework import serializers
from rest_framework.serializers import Serializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from seller_product.serializers import ProductSerializer, CommentSerializer

class Product_create_api(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            # overrding post request data with seller_id
            # getting id for foreign key seller_email in Product model
            data = request.data
            data['seller_email'] = request.user.id
        except:
            return Response(data = {'message':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProductSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(data = {'message': 'product saved sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(data = {'message': 'Invalid data entered'},status=status.HTTP_401_UNAUTHORIZED)

class Comment_add_api(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            data = request.data
            data['author'] = request.user.id
        except:
            return Response(data = {'message':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(data = {'message': 'added comment'}, status=status.HTTP_201_CREATED)
        return Response(data = {'message': 'Invalid data entered'},status=status.HTTP_401_UNAUTHORIZED)



