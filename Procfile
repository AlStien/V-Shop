release: python manage.py makemigrations base --no-input
release: python manage.py makemigrations seller_product --no-input
release: python manage.py migrate --no-input

web: gunicorn VShop.wsgi
