from django.db.models.base import Model
from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from seller_product.models import Comment, Product, Tag, OrderDetails

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['seller_email', 'name', 'price','brand', 'description']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class ProductsViewSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'brand', 'description']

class OrderViewSerializer(ModelSerializer):
    product = ProductsViewSerializer()
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity', 'price']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'product', 'rating', 'content']

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']
