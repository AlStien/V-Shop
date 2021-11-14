from faker import Faker
from random import random
from base.models import NewUser
from seller_product.models import Product

fake = Faker()
Faker.seed(313)
# For fake users
for i in range(10):

    name = fake.name()
    email = name + '@gmail.com'
    mobile = int(random()*(10**10))
    try:
        NewUser.objects.create(name = name,password='password', email =email, mobile = mobile)
    except:
        print("noooooooooo")

# for fake products
from faker import Faker

import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)

for i in range(10):

    name = fake.ecommerce_name()
    email = 'vshop.ecommerce.si@gmail.com'
    usr = NewUser.objects.get(email=email)
    price = int(random()*(10**4))
    brand = fake.ecommerce_name()
    description = fake.text()
    try:
        Product.objects.create(name = name, seller_email =usr, price = price, brand = brand, description = description)
    except:
        print("noooooooooo")