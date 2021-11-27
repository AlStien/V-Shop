# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# ------ base App Imports -------
from base.models import NewUser, OTP
from base.serializers import ProfileSerializer
from base.models import NewUser
# ------ seller_product App imports -------
from seller_product.models import Product 
from seller_product.serializers import ProductsViewSerializer

# ------ To Get List of all Sellers -------
class SellerListView(APIView):

    permission_classes = [AllowAny]
    def get(self, request, format = None):
        users = NewUser.objects.filter(is_seller = True)
        serializer = ProfileSerializer(users, many = True)
        return Response(serializer.data)

# ------ To Become Seller -------
class BecomeSellerView(APIView):

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

# ------ Seller Dashboard -------
class SellerProductsView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, format = None):
        user = request.user
        if user.is_seller:
            products = Product.objects.filter(seller_email = request.user.id)
            serializer = ProductsViewSerializer(products, many = True)
            return Response(serializer.data)
        else:
            return Response({'message': 'User Not a Seller'}, status=status.HTTP_403_FORBIDDEN)
