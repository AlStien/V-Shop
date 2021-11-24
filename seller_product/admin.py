from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.OrderDetails)
admin.site.register(models.Cart)
admin.site.register(models.Orders)
admin.site.register(models.Transaction)
admin.site.register(models.Coupon)
admin.site.register(models.Brands)

