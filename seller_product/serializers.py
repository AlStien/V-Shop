from django.db.models.base import Model
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, RelatedField
from base.models import NewUser
from seller_product.models import Comment, Product, Tag, OrderDetails, ProductImage
from seller_product.models import Brands, Comment, Product, Tag, OrderDetails
from base.api.serializers import AuthorIDSerializer
from collections import OrderedDict

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'product', 'rating', 'content']

class CommentSerializerForProductView(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author','rating', 'content']
    
    # def to_representation(self, instance):
    #     data =  super(CommentSerializerForProductView, self).to_representation(instance)
    #     name = NewUser.objects.get(id=instance['author']).name
    #     data['author'] = name
    #     return data 
    
class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['seller_email', 'name', 'price','brand', 'description','picture1','picture2', 'picture3', 'picture4']

    # def to_representation(self, instance):
    #     data = super(Auth).to_representation(instance)
    #     return super().to_representation(instance)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

class ProductsViewSerializer(ModelSerializer):

    tag_product = TagSerializer(many=True)
    comment_product = CommentSerializerForProductView(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'brand', 'avg_rating', 'description', 'picture1', 'picture2', 'picture3', 'picture4', 
        'comment_product', 'tag_product']

    def to_representation(self, instance):
        data = super(ProductsViewSerializer, self).to_representation(instance)
        
        # data is OrderedDict 
        # data['comment_product] is a list
        # accessing each via a loop
        # replacing every id by user name from NewUser Model
        
        try:
            i = 0
            avg_rating = 0

            for i in range(len(data['comment_product'])):
                author_id = data['comment_product'][i]['author']
                name = NewUser.objects.get(id=author_id).name
                data['comment_product'][i]['author'] = name

                avg_rating += data['comment_product'][i]['rating']

            data['avg_rating'] = int(avg_rating/(i+1))
        except:
            print('error')
        # tag = Tag.objects.get(id = id[0])
        # print(tag)
        # data_dict = data['tag_product']
        # data_dict[0] = tag
        return data
    # def to_representation(self, instance):
    #     # print("yayy")
    #     print("yayy")
    #     data = super(ProductsViewSerializer, self).to_representation(instance)
    #     product = Product.objects.get(id = instance['id'])
    #     product_images = ProductImage.objects.filter(product = product)
    #     data['product_images'] = product_images
    #     return data

class ProductImageSerializer(ModelSerializer):
    # picture = ProductImage.picture
    # product = ProductSerializer()
    class Meta:
        model = ProductImage
        fields = ['product', 'picture']

    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)

class OrderViewSerializer(ModelSerializer):
    product = ProductsViewSerializer()
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity', 'price']

class BrandsSeriaizer(ModelSerializer):
    class Meta:
        model = Brands
        fields = ['brand', 'image', 'product_count']