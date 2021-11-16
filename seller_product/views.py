from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.models import NewUser
from seller_product.models import (
            Comment, 
            Product, 
            Tag, 
            Cart, 
            OrderDetails,
            # ProductImage,
            Orders
)
from rest_framework import filters
from seller_product.serializers import (
    ProductSerializer, 
    CommentSerializer, 
    OrderViewSerializer,
    ProductsViewSerializer,
    # ProductImageSerializer,
)
from seller_product.serializers import ProductSerializer, CommentSerializer, TagSerializer, ProductsViewSerializer
from django_filters.rest_framework import DjangoFilterBackend

# is_seller check pending

class ProductsView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        try:
            if NewUser.objects.filter(id = request.user.id).exists():
                user = NewUser.objects.get(id = request.user.id)
                if user.is_seller:
                    data = Product.objects.exclude(seller_email = user.id)
            else:
                data = Product.objects.all()
            serializer = ProductsViewSerializer(data, many = True)
            return Response(serializer.data)
        except:
            return Response({'message': 'No Products Found'}, status=status.HTTP_404_NOT_FOUND)

class ProductDetailsView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format = None):
        try:
            product = Product.objects.get(id =request.data.get("id",))
            serializer = ProductsViewSerializer(product, many=False)
            return Response(serializer.data)
        except:
            return Response({'message': 'Product Not Found'}, status= status.HTTP_400_BAD_REQUEST)

    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]

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
            serializer_product = ProductSerializer(data = data)
            if serializer_product.is_valid():
                serializer_product.save()
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
            serializer = ProductSerializer(instance=product, data=request.data)
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

# class ProductImageView(APIView):
#     def post(self, request, format=None):
#         images = request.data.getlist('images')
#         product = Product.objects.get(seller_email = request.user.id, price = request.data.get("price",), 
#                                         name=request.data.get("name",))
#         for i in images:
#             ProductImage.objects.create(product = product, picture = i)
#         return Response(status=status.HTTP_202_ACCEPTED)

class SellerProductsView(APIView):
    def get(self, request, format = None):
        products = Product.objects.filter(seller_email = request.user.id)
        serializer = ProductsViewSerializer(products, many = True)
        return Response(serializer.data)


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

    def delete(self, request, format=None):
        data = request.data
        data['author'] = request.user.id
        try:
            comment = Comment.objects.get(id=data['id'])
            # To verify if the comment is published by the same author
            usr = NewUser.objects.get(id=data['author'])
            if str(comment.author) == str(usr.name):
                comment.delete()
                return Response(data={'message':'Comment deleted'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data={'message':'You can delete your comment only'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'message':'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = request.data
        data['author'] = request.user.id
        try:
            comment = Comment.objects.get(id=data['id'])
            # To verify if the comment is published by the same author
            usr = NewUser.objects.get(id=data['author'])
            if str(comment.author) == str(usr.name):
                serializer = CommentSerializer(comment, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(data={'message':'invalid data entered'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data={'message':'You can update your comment only'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'message':'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)

class Comment_view_api(APIView):
    # to get comments for a particular product
    def get(self, request, format=None):
        data = request.data
        comment = Comment.objects.filter(product=data['product'])
        if comment.exists():
            serializer = CommentSerializer(comment, many=True)
            return Response(serializer.data)
        else:
            return Response(data = {'message':'comments not found'}, status=status.HTTP_400_BAD_REQUEST)

class Tag_add_api(APIView):

    permission_classes = [IsAuthenticated]
    
    # for getting tags of a particular product
    def get(self, request, format=None):
        data = request.data
        tag = Tag.objects.filter(product=data['product'])
        if tag.exists():
            serializer = TagSerializer(tag, many=True)
            return Response(serializer.data)
        else:
            return Response(data = {'message':'product not found'}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response(data = {'message': 'tag saved sucessfully'}, status=status.HTTP_201_CREATED)
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
        if product.seller_email == request.user:
            return Response({'message': 'Seller Cannot Wishlist their own Product'}, status = status.HTTP_400_BAD_REQUEST)
        if NewUser.objects.filter(wishlist = product).exists():
            return Response({'message': 'Product Already in Wishlist'}, status=status.HTTP_208_ALREADY_REPORTED)
        product.wishlist_user.add(user)
        return Response(data = {'message': 'added product to wishlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request, format = None):
        user = NewUser.objects.get(email = request.user.email)
        product = Product.objects.get(id = request.data.get("id",))
        # user = NewUser.objects.filter(wishlist = product)
        print(user)
        if NewUser.objects.filter(wishlist = product).exists():
            product.wishlist_user.remove(user)
            return Response(data = {'message': 'removed product from to wishlist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Product Not in Wishlist'}, status = status.HTTP_404_NOT_FOUND)

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
            user_cart = Cart.objects.get(cart_user = user)
        else:
            user_cart = Cart.objects.create(cart_user = user)
        if product.seller_email == user.id:
            return Response({'message': 'Seller Cannot Wishlist their own Product'}, status = status.HTTP_400_BAD_REQUEST)
        if OrderDetails.objects.filter(product=product, cart_user = user_cart).exists():
            order = OrderDetails.objects.get(product=product, cart_user = user_cart)
            order.quantity = order.quantity + quantity
            order.save()
        else:
            OrderDetails.objects.create(product = product, cart_user = user_cart, 
                                quantity = quantity, price = (product.price * quantity))
        # products = Product.objects.filter(cart = user_cart)
        return Response(data = {'message': 'added product to cart'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, format = None):
        product = Product.objects.get(id = request.data.get("id",))
        user = NewUser.objects.get(id = request.user.id)
        user_cart = Cart.objects.get(cart_user = user)
        try:
            order = OrderDetails.objects.get(product=product, cart_user = user_cart)
            order.quantity = order.quantity - 1
            order.price = order.price - product.price
            if order.quantity > 0:
                order.save()
                return Response({'message': 'removed 1 item from Cart'}, status=status.HTTP_205_RESET_CONTENT)
            else:
                order.delete()
                return Response({'message': 'Product removed from Cart'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'No item Found'}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    def get(self, request, format=None):
        user = NewUser.objects.get(id = request.user.id)
        if Orders.objects.filter(user = user).exists():
            order = Orders.objects.get(user = user)
        else:
            order = Orders.objects.create(user = user)
        products = OrderDetails.objects.filter(orders = order)
        serializer = OrderViewSerializer(products, many = True)
        return Response(serializer.data)

    def put(self, request, format = None):
        user = request.user
        try:
            order = Orders.objects.get(user=user)
            order.delete()
            order = Orders.objects.create(user = user)
        except:
            order = Orders.objects.create(user = user)
        cart = Cart.objects.get(cart_user = user)
        if cart is not None:
            order_details = OrderDetails.objects.filter(cart_user = cart)
            for o in order_details:
                o.orders = order
                o.cart_user = None
                o.save()
            return Response({'message': 'Successfully Ordered'}, status= status.HTTP_202_ACCEPTED)
        return Response({},status = status.HTTP_403_FORBIDDEN)
class SearchProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsViewSerializer
    # djangoFilterBackend for categories/filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','tag_product__tag','brand']
    ordering_fields = ['name','price','brand']
    # default ordering
    ordering = ['price']
