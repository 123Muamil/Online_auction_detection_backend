
from rest_framework import generics,permissions
from rest_framework.response import Response
from users.permissions import IsBuyerUser, IsSellerUser,IsSellerOrAdmin
from .serializers import BuyerSerializer,SellerSerializer, UserSerilizer,ProductSerializer
from .models import Product
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import status
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