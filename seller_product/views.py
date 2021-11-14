from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from base.models import NewUser
from seller_product.models import Product, Tag, Cart, OrderDetails
from rest_framework import filters
from seller_product.serializers import (
    ProductSerializer, 
    CommentSerializer, 
    OrderViewSerializer,
    ProductsViewSerializer,
)
# is_seller check pending

class ProductView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        data = Product.objects.all()
        serializer = ProductsViewSerializer(data, many = True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        try:
            # overrding post request data with seller_id
            # getting id for foreign key seller_email in Product model
            data = request.data
            data['seller_email'] = request.user.id
            user = NewUser.objects.get(email = request.user.email)
        except:
            return Response(data = {'message':'user not found'},status=status.HTTP_401_UNAUTHORIZED)
        if user.is_seller:
            serializer = ProductSerializer(data = data)

            if serializer.is_valid():
                serializer.save()
                return Response(data = {'message': 'product saved sucessfully'}, status=status.HTTP_201_CREATED)
            return Response(data = {'message': 'Invalid data entered'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data = {'message': 'User not a seller'},status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=None):
        try:
            # overrding post request data with seller_id
            # getting id for foreign key seller_email in Product model
            data = request.data
            data['seller_email'] = request.user.id
            user = NewUser.objects.get(email = request.user.email)
        except:
            return Response(data = {'message':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

        if user.is_seller:
            product = Product.objects.get(id=data['id'])
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(data = {'message': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {'message': 'User not a seller'},status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        try:
            # overrding post request data with seller_id
            # getting id for foreign key seller_email in Product model
            data = request.data
            data['seller_email'] = request.user.id
            user = NewUser.objects.get(email = request.user.email)
        except:
            return Response(data = {'message':'user not found'},status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=data['id'])
            product.delete()
            return Response(data={'message':'Product deleted'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={'message':'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

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

class Tag_add_api(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        # getting product
        try:
            p = Product.objects.get(id=request.data['product'])
        except:
            return Response(data = {'message': 'product not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['tag']!='':
            # CASE 1 if same tag already exists
            try:
                t = Tag.objects.get(tag=request.data['tag'])
                t.product.add(p)
                return Response(data = {'message': 'product saved sucessfully'}, status=status.HTTP_201_CREATED)

            # CASE 2 if tag doesn't exist 
            except:
                t = Tag.objects.create(tag=request.data['tag'])
                t.product.add(p)
                return Response(data = {'message': 'product saved sucessfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data = {'message': 'enter a tag'}, status=status.HTTP_400_BAD_REQUEST)

class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = NewUser.objects.get(id = request.user.id)
        products = Product.objects.filter(wishlist_user = user)
        serializer = ProductsViewSerializer(products, many = True)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        user = NewUser.objects.get(email = request.user.email)
        product = Product.objects.get(id = request.data.get("id",))
        product.wishlist_user.add(user)
        return Response(data = {'message': 'added product to wishlist'}, status=status.HTTP_201_CREATED)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = NewUser.objects.get(id = request.user.id)
        if Cart.objects.filter(cart_user = user).exists():
            cart = Cart.objects.get(cart_user = user)
        else:
            cart = Cart.objects.create(cart_user = user)
        products = OrderDetails.objects.filter(cart_user = cart)
        serializer = OrderViewSerializer(products, many = True)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        product = Product.objects.get(id = request.data.get("id",))
        quantity = int(request.data.get("quantity",))
        user = NewUser.objects.get(id = request.user.id)
        if Cart.objects.filter(cart_user = user).exists():
            print('yayy')
            user_cart = Cart.objects.get(cart_user = user)
        else:
            print('ok')
            user_cart = Cart.objects.create(cart_user = user)
        OrderDetails.objects.create(product = product, cart_user = user_cart, 
                            quantity = quantity, price = (product.price * quantity))
        # products = Product.objects.filter(cart = user_cart)
        return Response(data = {'message': 'added product to cart'}, status=status.HTTP_201_CREATED)

class SearchProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsViewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']