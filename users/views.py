
from rest_framework import generics,permissions
from rest_framework.response import Response
from users.permissions import IsBuyerUser, IsSellerUser,IsSellerOrAdmin
from .serializers import BuyerSerializer,SellerSerializer, UserSerializer, UserSerilizer,ProductSerializer
from .models import Product, User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import status
from .models import Seller
import hashlib
from joblib import load
from django.db.models import Count
from users import models
# Load the trained model
# model = load('./model.pkl')
# print("The model is:",model)
class BuyerView(generics.GenericAPIView):
    serializer_class=BuyerSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            name=request.data.get('name'),
            email=request.data.get('email'),
            id_card=request.data.get('id_card'),
            phone_number=request.data.get('phone_number'),
            address=request.data.get('address')
        )
        return Response({
            "user": UserSerilizer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "Buyer account created successfully"
        })
class SellerView(generics.GenericAPIView):
    serializer_class=SellerSerializer
    def post(self, request, *args, **kwargs):
        # print(request.data)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerilizer(user,context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"Seller account created successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_buyer': user.is_buyer,
            "is_seller":user.is_seller,
            "is_superuser":user.is_superuser,
            "username":user.username,
        })
class LogoutView(APIView):
    def post(self,request,format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
    
class BuyerOnlyView(generics.RetrieveAPIView):
    serializer_class = UserSerilizer 
    permission_classes=[permissions.IsAuthenticated&IsBuyerUser]
    
    def get_object(self):
        return self.request.user
    
class SellerOnlyView(generics.RetrieveAPIView):
    serializer_class = UserSerilizer  
    permission_classes = [permissions.IsAuthenticated & IsSellerUser]
    
    def get_object(self):
        return self.request.user
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated & IsSellerOrAdmin]
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated & IsSellerOrAdmin]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]
class AllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
class ProductBySellerListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            sellers = User.objects.filter(is_seller=True)
            products_by_seller = {}

            for seller in sellers:
                seller_products = seller.products.all()
                products_by_seller[seller.username] = ProductSerializer(seller_products, many=True).data

            return products_by_seller
        else:
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)
class DetectDuplicateSellerAccounts(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = load('./model.pkl')
    def get(self, request):
        duplicate_accounts = []
        sellers = Seller.objects.all()
        for seller in sellers:
            if seller.id_card:
                features = self.extract_features(seller)
                
                try:
                    is_duplicate = self.model.predict([features])[0]
                    if is_duplicate:
                        duplicate_accounts.append(seller)
                except Exception as e:
                    print(f"Error predicting for seller {seller.id}: {e}")

        serializer = SellerSerializer(duplicate_accounts, many=True)
        return Response(serializer.data)

    def extract_features(self, seller):
        username = seller.user.username if seller.user.username else ''
        address = seller.address if seller.address else ''
        name = seller.name if seller.name else ''
        email = seller.email if seller.email else ''
        phone_number = seller.phone_number if seller.phone_number else ''
        
        dummy_mac_address = "00:00:00:00:00:00"

        username_encoded = username.encode()
        address_encoded = address.encode()
        name_encoded = name.encode()
        email_encoded = email.encode()
        phone_number_encoded = phone_number.encode()
        dummy_mac_address_encoded = dummy_mac_address.encode()

        device_id = hashlib.md5(username_encoded + address_encoded).hexdigest()
        device_id_normalized = int(device_id, 16) / (10 ** 38)

        if seller.id_card:
            user_id_hash = self.hash_user_id(seller.id_card)
            user_id_hash_normalized = user_id_hash / (10 ** 38)
        else:
            user_id_hash_normalized = 0

        features = [
            device_id_normalized,
            user_id_hash_normalized,
            self.hash_categorical(name_encoded),
            self.hash_categorical(email_encoded),
            self.hash_categorical(phone_number_encoded),
            self.hash_categorical(address_encoded),
            seller.date_of_birth.toordinal() if seller.date_of_birth else 0,
            self.hash_categorical(dummy_mac_address_encoded),
        ]

        return features

    def hash_user_id(self, user_id):
        hash_object = hashlib.md5(user_id.encode())
        hash_digest = hash_object.hexdigest()
        hash_int = int(hash_digest, 16)
        return hash_int

    def hash_categorical(self, value):
        if value:
            return int(hashlib.md5(value).hexdigest(), 16) / (10 ** 38)
        return 0
class DuplicateSellerCheckView(APIView):
    def get(self, request, *args, **kwargs):
        # Aggregate sellers by ID card and count them
        duplicate_sellers = Seller.objects.values('id_card').annotate(count=Count('id_card')).filter(count__gt=1)
        
        if duplicate_sellers.exists():
            # Find all sellers with these duplicate ID cards
            duplicate_sellers_list = Seller.objects.filter(id_card__in=[item['id_card'] for item in duplicate_sellers])
            return Response({
                "message": "Duplicate seller accounts found",
                "duplicates": SellerSerializer(duplicate_sellers_list, many=True).data
            }, status=status.HTTP_200_OK)
        else:
            # If no duplicates found, return a message indicating no duplicates
            return Response({
                "message": "No duplicate seller accounts found"
            }, status=status.HTTP_200_OK)