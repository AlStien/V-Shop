from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from base.models import NewUser
from seller_product.models import Comment, Product, Tag
from rest_framework import filters
from seller_product.serializers import ProductSerializer, CommentSerializer, TagSerializer, ProductsViewSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# is_seller check pending

class ProductsView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        data = Product.objects.all()
        serializer = ProductsViewSerializer(data, many = True)
        return Response(serializer.data)
    
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
            product = Product.objects.get(product_id=data['product_id'])
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
            product = Product.objects.get(product_id=data['product_id'])
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
            p = Product.objects.get(product_id=request.data['product'])
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
        product = Product.objects.get(product_id = request.data.get("id",))
        product.wishlist_user.add(user)
        return Response(data = {'message': 'added product to wishlist'}, status=status.HTTP_201_CREATED)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = NewUser.objects.get(id = request.user.id)
        products = Product.objects.filter(cart_user = user)
        serializer = ProductsViewSerializer(products, many = True)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        user = NewUser.objects.get(email = request.user.email)
        product = Product.objects.get(product_id = request.data.get("id",))
        product.cart_user.add(user)
        return Response(data = {'message': 'added product to cart'}, status=status.HTTP_201_CREATED)

class SearchProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsViewSerializer
    # djangoFilterBackend not working
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name','tag_product__tag','brand']
    ordering_fields = ['name','price','brand']
    # default ordering
    ordering = ['price']
