from rest_framework.serializers import ModelSerializer
from seller_product.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['seller_email', 'name', 'price', 'brand', 'description']
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data) 
