from django.http import response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.models import NewUser
from seller_product.models import (
            Brands,
            Comment, 
            Product, 
            Tag, 
            Cart, 
            OrderDetails,
            ProductImage,
            Orders,
            Transaction,
            Coupon
)
from rest_framework import filters
from seller_product.serializers import (
    BrandsSeriaizer,
    ProductSerializer, 
    CommentSerializer, 
    OrderViewSerializer,
    ProductsViewSerializer,
    # OrderGetSerializer
    ProductImageSerializer,
    TagSerializer,
)
# from seller_product.serializers import ProductSerializer, CommentSerializer, TagSerializer, ProductsViewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from random import choice, random, randint
from VShop.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives

def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['product'] = property_id
    dict['picture'] = image
    return dict

def confMail(email):
    from_email, to = EMAIL_HOST_USER, email
    subject = f"Order Confirmation for {NewUser.objects.get(email = email).name}"
    text_content = f'Thank You for Ordering with Us. If You face any problem with the order, please feel free to contact us. Your Order is on the way with Our Best Delivery Service. With Regards. V-SHOP'
    html_content = f'<span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; line-height: 0.9em;"><p>Thank You for ordering with us. If You Face any problem, Please feel free to Contact Us</p><p>Your Order is On the Way. You Can View Your Orders through the Website or <a href="https://v-shop.netlify.app/orders" style="color: #3fa0cf">Click Here</a></p><p style="font-size: 18px;">WITH REGARDS</p><p style="line-height: 1.2em;"><a href="https://v-shop.netlify.app/profile"><strong style="font-size: 20px; background: #0811ed; padding: 4px 10px; color: white; border-radius: 20px;">V-SHOP</strong></a></p></span>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class ProductsView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        try:
            if NewUser.objects.filter(id = request.user.id).exists():
                user = NewUser.objects.get(id = request.user.id)
                if user.is_seller:
                    data = Product.objects.exclude(seller_email = user.id)
            else:
                print("gg")
                data = Product.objects.all()
            serializer = ProductsViewSerializer(data, many = True)
            return Response(serializer.data)
        except:
            return Response({'message': 'No Products Found'}, status=status.HTTP_404_NOT_FOUND)

class ProductDetailsView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format = None):
        try:
            product = Product.objects.get(id = int(request.data.get("id",)))
            product_images = ProductImage.objects.filter(product = product)
            serializer = ProductsViewSerializer(product, many=False)
            try:
                serializer_image = ProductImageSerializer(product_images, many = True)
                print(serializer_image)
                Serializer_list = [serializer.data, serializer_image.data]

                content = {
                    'status': 1, 
                    'responseCode' : status.HTTP_302_FOUND, 
                    'data': Serializer_list,
                }
                return Response(content)
            except:
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

class ProductImageView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        # product = Product.objects.get(id = request.data.get('id',))
        product = data.get('id',)
        images = dict((request.data).lists())['picture']
        print(images)
        arr = []
        for i in images:
            print(f'i {i}')
            # ProductImage.objects.create(product = product, picture = i)
            modified_data = modify_input_for_multiple_files(product, i)
            print(f'yayy {modified_data}')
            serializer = ProductImageSerializer(data = modified_data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                print(f'sd {serializer.data}')
                arr.append(serializer.data)
                # return Response(serializer.data)
            print(f'arr {arr}')
        return Response(arr)

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
    permission_classes = [AllowAny,]
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
        if NewUser.objects.filter(wishlist = product, email = request.user.email).exists():
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
            order.price = order.price + (quantity * product.price)
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

class CartDeleteView(APIView):

    def delete(self, request, format = None):
        product = Product.objects.get(id = request.data.get("id",))
        user = NewUser.objects.get(id = request.user.id)
        user_cart = Cart.objects.get(cart_user = user)
        try:
            order = OrderDetails.objects.get(product=product, cart_user = user_cart)
            order.delete()
            return Response({'message': 'Product removed from Cart'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'No item Found'}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    def get(self, request, format=None):
        user = request.user
        if Orders.objects.filter(user = user).exists():
            order = Orders.objects.filter(user = user)
        else:
            order = Orders.objects.create(user = user)
        order_last = Orders.objects.create(user = user, amount = 100)
        for o in order:
            details = OrderDetails.objects.filter(orders = o)
            for detail in details:
                print(detail)
                detail.orders = Orders.objects.filter(user = user).last()
                print(detail.orders.amount)
                detail.save()
        order = Orders.objects.filter(user = user)
        order[0].delete()
        products = OrderDetails.objects.filter(orders = order_last)
        serializer = OrderViewSerializer(products, many = True)
        return Response(serializer.data)

    def put(self, request, format = None):
        user = request.user
        # try:
        #     order = Orders.objects.get(user=user)
        #     order.delete()
        #     order = Orders.objects.create(user = user)
        # except:
        order = Orders.objects.create(user = user)
        cart = Cart.objects.get(cart_user = user)
        if cart is not None:
            order_details = OrderDetails.objects.filter(cart_user = cart)
            for o in order_details:
                o.orders = order
                o.cart_user = None
                o.save()
            confMail(request.user.email)
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

class SearchFilterProduct(APIView):
    def get(self, request, format=None):
        data = request.data
        if 'category_tag' in data:
            filter = data.get('category_tag')
            # for tag filtering
            try:
                filtered_products = Product.objects.filter(tag_product__tag__iexact = filter)
                serializer = ProductsViewSerializer(filtered_products, many = True)
                if serializer.data == []:
                    return Response({'message':'Not matching products with given tag found'})
                return Response(serializer.data)
            except:
                return Response({'message':'errrrrrr'})
        # for brand filtering
        filter = request.data.get('category_brand')
        try:
            filtered_products = Product.objects.filter(brand__iexact = filter)
            serializer = ProductsViewSerializer(filtered_products, many = True)
            if serializer.data == []:
                return Response({'message':'Not matching products with given brand found'})
            return Response(serializer.data)
        except:
            return Response({'message':'errrrrrr'})

# REDIRECT FROM CART

def txn_id_generator(id,amount):
    t = str(timezone.now())
    t = t.replace(' ','').replace('-','').replace(':','').replace('.','').replace('+','')
    t = str(id)+'U'+ t +'A'+ str(amount)
    # example 2U202111181756094092860000A5675
    return t

class CheckoutTransaction(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        entered_amount = data.get('amount')
        payment_method = data.get('payment_method')
        txn_id = txn_id_generator(request.user.id,entered_amount)
        amount_paid = entered_amount
        # try:
        #     coupon_code = data.get('code')
        #     coupon = coupon.objects.get(code=coupon_code)
        # except:
        #     coupon_msg = 'Enter valid coupon code'
        
        # try:
            # cart_amount = Cart.objects.get(cart_user = request.user).amount
            # if cart_amount==entered_amount:
            #     print('matched')
        try:
            Transaction.objects.create(user=request.user, transaction_id=str(txn_id), amount=int(entered_amount), payment_method=payment_method)
            try:
                coupon_code = data.get('code')
                coupon = Coupon.objects.get(code=coupon_code)
                time_now = timezone.now()
                if coupon.expiry> time_now:
                    coupon.used+=1
                    coupon.save()
                    amount_paid = entered_amount*0.95
                    coupon_msg = 'coupon applied 5% discount'
                else:
                    coupon_msg = 'coupon expired'
            except:
                coupon_msg = 'Enter valid coupon code'
            return Response({'message':'Transaction Successful',
                            'txn_id':txn_id,
                            'user':request.user.name,
                            'amount_paid':amount_paid,
                            'payment_method':payment_method,
                            'coupon_msg':coupon_msg}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'Invalid data entered'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'message':'Enter correct amount'}, status=status.HTTP_400_BAD_REQUEST)
        # except:
            # return Response({'message':'Cart not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

def send_coupon():
    # generating coupon code
    def generate_code():
        code = ''
        type = '01'
        for i in range(6):
            if choice(type)=='0':
                code += choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            else:
                code += str(choice([i for i in range (10)]))
        # example UN1AJ9
        return code
    
    code = generate_code()

    # to check if randomly generated coupon code exists in database
    c = Coupon.objects.filter(code = code)
    while c.count() != 0:
        print("code exists")
        code = generate_code()
        c = Coupon.objects.filter(code = code)

    try:
        Coupon.objects.create(code = code)
    except:
        print("error processing coupon code")

    from_email, to = EMAIL_HOST_USER, [NewUser.objects.filter(is_seller=False)[i].email for i in range(NewUser.objects.filter(is_seller=False).count())]
    subject = "coupon for V-Shop"
    text_content = f'coupon{code}.\nValid for only 7 days.'
    html_content = f'<span style="font-family: Arial, Helvetica, sans-serif; font-size: 16px;"><p style="font-size: 18px;">GREETINGS FROM VSHOP</p><p>Your coupon code for 5% dicount on V-Shop is <strong style="font-size: 18px;">{code}</strong>.</p><p>Valid for only 7 days</p></span>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return to

class SendCoupon(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_staff:
            recepients_list = send_coupon()
            return Response({'message':'Sent coupon mail to following users','recepients_list':recepients_list})
        else:
            return Response({'message':'Only staff members can send coupons'})
# NOW REDIRECT TO ORDER CHECKOUT is_paid check ???

def update_brands_data():
    run = randint(1,10)
    # 20% chances of updating database
    if run <=2:
        print("run")
        p = Product.objects.all()
        count = p.count()
        try:
            # adding brands to table
            for i in range(count):
                brand = p[i].brand
                Brands.objects.get_or_create(brand=brand.lower())
            # adding product count
            for i in range(count):
                b = Brands.objects.get(brand__iexact=p[i].brand)
                b.product_count +=1                         
                b.save()
            # deleting entries with zero products
            Brands.objects.filter(product_count=0).delete()
        except:
            pass

class ShowBrands(APIView):

    def get(self, request, format=None):
# --------------------SLOW QUERY FUNCTION---------------------------------------# 
        update_brands_data()
        brands = Brands.objects.all()
        serializer = BrandsSeriaizer(brands, many=True)
        return Response(serializer.data)
