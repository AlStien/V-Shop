from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from base.models import NewUser
from django.core.validators import MaxLengthValidator

# a seller can have many products  so many-to-one relationship
class Product(models.Model):
    # product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_email = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="seller_email")
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    no_of_sales = models.IntegerField(default=0)
    picture1 = models.ImageField(upload_to = 'products' ,default = f'products/default.png')
    picture2 = models.ImageField(upload_to = 'products' , null = True)
    picture3 = models.ImageField(upload_to = 'products' , null = True)
    picture4 = models.ImageField(upload_to = 'products' , null = True)

    wishlist_user = models.ManyToManyField(NewUser, related_name='wishlist', blank=True)
    # cart = models.ManyToManyField(Cart, related_name='cart')

    def __str__(self):
        return self.name

    def pid(self):
        return self.product_id

    def total_income(self):
        return self.no_of_sales*self.price

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=CASCADE, null=True, blank=True)
#     picture = models.ImageField(upload_to = 'products' ,default = f'products/default.png', null = True

#     def picture(self):
#         return self.picture

class Cart(models.Model):
    cart_user = models.OneToOneField(NewUser, related_name='user', on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.cart_user.name

class Orders(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.product.name

class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodcut')
    cart_user = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order_details', null=True, blank=True)
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


# class Orders(models.Model):

#     orders_user = models.ForeignKey(NewUser, related_name='user')
#     ordered_products = models.sManyToManyField(Product, related_name='products')

# a product can have many comments so many-to-one relationship
class Comment(models.Model):

    rating_choices = [
        (1,'poor'),
        (2,'unsatisfactory'),
        (3,'average'),
        (4,'good'),
        (5,'excellent')
    ]

    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="comment_product")
    author = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="author")
    # rating from 1 to 5 fromt end validation req
    # rating = models.IntegerField(default=1,validators=[MaxLengthValidator(1)])
    rating = models.CharField(max_length=1, choices=rating_choices, default=1)
    content = models.CharField(max_length=300)

    def __str__(self):
        return self.content

# a product can have many tags so many-to-one relationship
class Tag(models.Model):
    product = models.ManyToManyField(Product, related_name="tag_product")
    tag = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.tag
