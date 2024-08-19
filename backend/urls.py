from django.urls import path
from .views import ProductAPI, GetToken, UserRegistration, CartAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path('products/', ProductAPI.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductAPI.as_view(), name='product-detail'),
    
    path('token/', GetToken.as_view(), name='get-token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    
    path('register/', UserRegistration.as_view(), name='user-registration'),
    
    path('cart/', CartAPIView.as_view(), name='cart-detail'),
    path('cart/<int:pk>/', CartAPIView.as_view(), name='cart-item')
]
