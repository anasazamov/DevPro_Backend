from rest_framework import serializers
from .models import Product, Cart, CartItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=False)
    product = ProductSerializer(read_only=True, many=False)

    class Meta:
        model = CartItem
        fields = "__all__"