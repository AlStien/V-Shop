from faker import Faker
from random import random
from random import choice, randint
from base.models import NewUser
from seller_product.models import Product, Comment, Tag, ProductImage

fake = Faker()
Faker.seed(313)

# For fake normal users
for i in range(100):

    name = fake.name()
    email = name.replace(' ','') + '@user.com'
    mobile = int(random()*(10**10))
    gender = choice(['M','F','O'])
    password = 'pbkdf2_sha256$260000$SSLDjLy78kQuOd6LKk9LjX$V0zbVWP+RYitfN9Ag3884SrhE6GmdGQT21NfhhAB0gI='
    try:
        NewUser.objects.create(name = name, password=password, email =email, mobile = mobile, gender=gender, is_active=True, is_verified=True)
    except:
        print("noooooooooo")

# For fake sellers
for i in range(100):

    name = 'Seller '+fake.name()
    email = name.replace(' ','') + '@seller.com'
    mobile = int(random()*(10**10))
    gender = choice(['M','F','O'])
    password = 'pbkdf2_sha256$260000$SSLDjLy78kQuOd6LKk9LjX$V0zbVWP+RYitfN9Ag3884SrhE6GmdGQT21NfhhAB0gI='
    try:
        NewUser.objects.create(name = name, password=password, email =email, mobile = mobile, gender=gender, is_active=True, is_verified=True, is_seller=True)
    except:
        print("noooooooooo")


# for fake products
from faker import Faker

import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)

# FOR ADDING PRODUCTS
for i in range(10):

    name = fake.ecommerce_name()
    query = NewUser.objects.filter(name__startswith="Seller")
    email = query[randint(0,40)].email
    usr = NewUser.objects.get(email=email)
    # IMAGE FIELD
    price = int(random()*(10**4))
    brand = fake.ecommerce_name()
    description = fake.text()
    try:
        product_obj = Product.objects.create(name = name, seller_email =usr, price = price, brand = brand, description = description)
        print("product added")
        # ADDING IMAGE
        for j in range(2):
            try:
                pic = choice([i for i in range(1,11)])
                product_img = ProductImage.objects.create(product=product_obj, picture='products/p'+str(pic)+'.jpg')
                print("image added")    
            except:
                print("image not added")    

        # ADDING COMMENTS
        for j in range(2):
            try:
                rating = choice([1,2,3,4,5])
                comment_obj = Comment.objects.create(product=product_obj, author=usr, content=fake.text(), rating=rating)
                print("comment added")
            except:
                print("comment not added")
        
        # ADDING TAG
        for k in range(3):
            generated_tag = fake.ecommerce_name()
            # CASE 1 if tag exists
            try:
                t = Tag.objects.get(tag=generated_tag)
                t.product.add(product_obj)
                print("Adding product to existing tag")
            # CASE 2 if tag doesn't exist 
            except:
                t = Tag.objects.create(tag=generated_tag)
                t.product.add(product_obj)
                print("Adding product to new tag")

    except:
        print("Product not added")



