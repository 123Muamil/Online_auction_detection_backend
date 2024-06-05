from django.contrib import admin
from .models import User,Buyer,Seller,Product
# Register your models here.
admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Product)