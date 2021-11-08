from django.db import models
import uuid
from base.models import NewUser
from django.core.validators import MaxLengthValidator

# a seller can have many products  so many-to-one relationship
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_email = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="seller_email")
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    no_of_sales = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def pid(self):
        return self.product_id

    def total_income(self):
        return self.no_of_sales*self.price

# a product can have many comments so many-to-one relationship
class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="comment_product")
    author = models.ForeignKey(NewUser,on_delete=models.CASCADE, related_name="author")
    # rating from 1 to 5 fromt end validation req
    # rating = models.IntegerField(default=1,validators=[MaxLengthValidator(1)])
    rating = models.IntegerField(default=1)
    content = models.CharField(max_length=300)

# a product can have many tags so many-to-one relationship
class Tag(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="tag_product")
    tag = models.CharField(max_length=30)
