from django.db import models
from base.models import NewUser
from django.utils import timezone

# ------ Product Model -------
class Product(models.Model):

    # A Seller can have Multiple Products, so Foreign Key
    seller_email = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="seller_email")
    # ------ Basic Product Description -------
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    stock = models.IntegerField(default=0)
    picture1 = models.ImageField(upload_to = 'products' ,default = f'products/default.png')
    picture2 = models.ImageField(upload_to = 'products' , null = True, blank = True)
    picture3 = models.ImageField(upload_to = 'products' , null = True, blank = True)
    picture4 = models.ImageField(upload_to = 'products' , null = True, blank = True)

    avg_rating = models.IntegerField(default=0)
    wishlist_user = models.ManyToManyField(NewUser, related_name='wishlist', blank=True)

    def __str__(self):
        return self.name

    def pid(self):
        return self.product_id

    def total_income(self):
        return self.no_of_sales*self.price

# # ------ Separate Model for Product Images -------
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True)
#     picture = models.ImageField(upload_to = 'products' ,default = f'products/default.png')

#     def __str__(self):
#         return self.product.name

# ------ For User Cart -------
class Cart(models.Model):
    cart_user = models.OneToOneField(NewUser, related_name='user', on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cart_user.name

# ------ For User Orders -------
class Orders(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.name

# ------ A single Order detail entity to use for Orders and Cart -------
class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodcut')
    cart_user = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_details', null=True, blank=True)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    updated = models.DateTimeField(auto_now = True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

# ------ Rating and Reviews Model -------
class Comment(models.Model):

    rating_choices = [
        (1,'poor'),
        (2,'unsatisfactory'),
        (3,'average'),
        (4,'good'),
        (5,'excellent')
    ]

    # a product can have many Reviews and Rating so many-to-one relationship
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="comment_product")
    author = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="author")
    # rating from 1 to 5 fromt end validation req
    # rating = models.IntegerField(default=1,validators=[MaxLengthValidator(1)])
    rating = models.IntegerField(choices=rating_choices, default=1)
    content = models.CharField(max_length=300)

    def __str__(self):
        return self.content

# ------ Tags for Products -------
class Tag(models.Model):
    # a product can have many tags so many-to-one relationship
    product = models.ManyToManyField(Product, related_name="tag_product")
    tag = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.tag

# ------ Transactions after Checkout -------
class Transaction(models.Model):
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="transaction_user")
    transaction_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20)

    def __str__(self):
        return self.transaction_id

# ------ Coupon Model -------
class Coupon(models.Model):
    
    def set_expiry():
        return timezone.now() + timezone.timedelta(days=7)
        
    code = models.CharField(max_length=6, unique=True)
    expiry = models.DateTimeField(default=set_expiry())
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.code

# ------ Brands Model -------
class Brands(models.Model):
    brand = models.CharField(max_length=50)
    image = models.ImageField(upload_to = 'brands' ,default = f'brands/wp6611732_wru2sc')
    product_count = models.IntegerField(default=0)

    def __str__(self):
        return self.brand
