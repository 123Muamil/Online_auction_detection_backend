
from rest_framework import serializers
from users.models import User,Buyer,Seller,Product
# from datetime import timezone
class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
class SellerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=254, required=True)
    id_card = serializers.CharField(max_length=50, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [ 'email', 'password', 'password2', 'name', 'id_card', 'phone_number', 'address', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            # username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
    
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        user.set_password(password)
        user.is_seller = True  # Assuming this field exists in the User model
        user.save()
        
        Seller.objects.create(
            user=user,
            name=self.validated_data.get('name', ''),
            email=self.validated_data.get('email', ''),
            id_card=self.validated_data.get('id_card'),
            phone_number=self.validated_data.get('phone_number'),
            address=self.validated_data.get('address', ''),
            date_of_birth=self.validated_data.get('date_of_birth', None),
            # account_created=timezone.now()  # This will automatically set the current time
        )
        
        return user

class BuyerSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=254, required=True)
    id_card = serializers.CharField(max_length=50, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'name', 'id_card', 'phone_number', 'address', 'date_of_birth']
        extra_kwargs = {
            'password': {'write_only': True}
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
        user.is_buyer = True  # Assuming this field exists in the User model
        user.save()
        
        Buyer.objects.create(
            user=user,
            name=self.validated_data.get('name', ''),
            email=self.validated_data.get('email', ''),
            id_card=self.validated_data.get('id_card', ''),
            phone_number=self.validated_data.get('phone_number', ''),
            address=self.validated_data.get('address', ''),
            date_of_birth=self.validated_data.get('date_of_birth', None),
            # account_created=timezone.now()  # This will automatically set the current time
        )
        
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
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'