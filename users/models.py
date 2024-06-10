from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    is_buyer=models.BooleanField(default=False)
    is_seller=models.BooleanField(default=False)
    def __str__(self):
        return self.username
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

           
class Buyer(models.Model):
    user = models.OneToOneField(User, related_name='buyer', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True) 
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)  
    id_card = models.CharField(max_length=50, blank=True, null=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    account_created = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.user.username
class Seller(models.Model):
    user = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True) 
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)  
    id_card = models.CharField(max_length=50, blank=True, null=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    account_created = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.user.username
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', limit_choices_to={'is_seller': True})  # Restrict to sellers
    name = models.CharField(max_length=255)
    description = models.TextField()
    min_bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
