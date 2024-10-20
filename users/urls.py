from django.urls import path
from .views import AllUsersView,DuplicateSellerCheckView, BuyerView,SellerView,CustomAuthToken,BuyerOnlyView,SellerOnlyView,ProductCreateView,ProductRetrieveUpdateDestroyView,ProductListView,AllUsersView,ProductBySellerListView,DetectDuplicateSellerAccounts
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
      path('users/', AllUsersView.as_view(), name='all_users'),
      path('by-seller/', ProductBySellerListView.as_view(), name='products-by-seller'),
      path('detect_duplicate_sellers/', DetectDuplicateSellerAccounts.as_view(), name='detect_duplicate_sellers'),
      path('check-duplicates/', DuplicateSellerCheckView.as_view(), name='check-duplicates'),
]
# Serve media files during development




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)