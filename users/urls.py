from django.urls import path
from .views import BuyerView,SellerView,CustomAuthToken,BuyerOnlyView,SellerOnlyView,ProductCreateView,ProductRetrieveUpdateDestroyView,ProductListView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
      path('singup/buyer/',BuyerView.as_view()),
      path('singup/seller/',SellerView.as_view()),
      path('login/', CustomAuthToken.as_view()),
      path('buyer/dashboard/',BuyerOnlyView.as_view()),
      path('seller/dashboard/',SellerOnlyView.as_view()),
      path('products/', ProductCreateView.as_view(), name='product-create'),
      path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
      path('all-products/', ProductListView.as_view(), name='all-products'),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)