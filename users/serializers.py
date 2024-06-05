
from rest_framework import serializers
from users.models import User,Buyer,Seller,Product
class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
class SellerSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model=User
        fields='__all__'
    extra_kwargs={
        'password':{
            'write_only':True
        }
    }
    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
    
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        user.set_password(password)
        user.is_seller = True
        user.save()
        Seller.objects.create(user=user)
        return user

class BuyerSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model=User
        fields='__all__'
    extra_kwargs={
        'password':{
            'write_only':True
        }
    }
    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
    
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        user.set_password(password)
        user.is_buyer = True
        user.save()
        Buyer.objects.create(user=user)
        return user
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    seller_username = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ('id', 'seller_username', 'name', 'description', 'min_bid_amount','category','image')