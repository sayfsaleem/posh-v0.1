from django.urls import path
from .views import CustomerRegistrationView, StoreOwnerRegistrationView,AuthorizationView,ProductMarketListView,WholeSellerRegistrationView,MarkTokensView,get_datas,UserDataView,MarkProductRedeemedView
urlpatterns = [
    path('customer-register/', CustomerRegistrationView.as_view(), name='customer-registration'),
    path('store-owner-register/', StoreOwnerRegistrationView.as_view(), name='store-owner-registration'),
    path('wholeseller-register/',WholeSellerRegistrationView.as_view(),name='wholeseller-registration'),
    path('auth/', AuthorizationView.as_view(), name='authorization'),
    path('productmarket/', ProductMarketListView.as_view(), name='product'),
    path('customer-scan/', MarkTokensView.as_view(), name='customer-scan'),
    path('check/',get_datas,name='check'),
    path('user-info/',UserDataView.as_view(), name='user-info'),
    path('product-redeem/',MarkProductRedeemedView.as_view(), name='product-redeemed'),
]
