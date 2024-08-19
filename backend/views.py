from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, UserSerializer
from .models import Product, Cart, CartItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
# Create your views here.

class ProductAPI(APIView, PageNumberPagination):
    @swagger_auto_schema(
        operation_summary="Get all products or a single product by ID",
        operation_description="Retrieve all products if no ID is provided, or a single product by its ID.",
        responses={
            200: ProductSerializer(many=True),
            404: 'Product not found'
        })

    def get(self, request: Request, pk=False):

        if pk:
            product = Product.objects.filter(id=pk)
            if product.exists():
                product = product.first()
                serializer = ProductSerializer(product)
                return Response(serializer.data, status.HTTP_200_OK)
            return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        paginated_data = self.paginate_queryset(serializer.data,request)
        return self.get_paginated_response(paginated_data)
        
    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Add a new product to the database.",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer(),
            400: 'Invalid data'
        }
    )
    
    def post(self, request: Request):
        
        data = request.data
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Update an existing product",
        operation_description="Update an existing product by its ID.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer(),
            404: 'Product not found',
            400: 'Invalid data'
        }
    )
    def put(self, request: Request, pk=False):

        data = request.data

        if pk:
            product = Product.objects.filter(id=pk)
            if product.exists():
                product = product.first()
                serializer = ProductSerializer(product,data=data)
                if serializer.is_valid():
                    return Response(serializer.data, status.HTTP_200_OK)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Not found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "ID is requirement"}, status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_summary="Delete a product",
        operation_description="Delete an existing product by its ID.",
        responses={
            204: 'Product successfully deleted',
            404: 'Product not found'
        }
    )
    def delete(self, request: Request, pk=False):
        """
        Mavjud mahsulotni o'chiradi. `pk` parametri orqali berilgan ID'ga mos keluvchi mahsulotni topib, o'chiradi.
        """

        if pk:
            product = Product.objects.filter(id=pk)
            if product.exists():
                product = product.first()
                product.delete()
                return Response({"message": "The product was successfully deleted"}, status.HTTP_204_NO_CONTENT)

        return Response({"message": "ID is requirement"}, status.HTTP_404_NOT_FOUND)
    
class GetToken(APIView):
    
    authentication_classes = [BasicAuthentication]

    @swagger_auto_schema(
        operation_summary="Get JWT tokens for authenticated user",
        operation_description="Retrieve JWT access and refresh tokens for authenticated user using Basic Authentication.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username of User'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password of User')
            },
        ),
        responses={
            200: 'Token retrieved successfully',
            401: 'Unauthorized'
        }
    )
    def post(self, request: Request):
        data = request.data
        username = data.get("username", "")
        password = data.get("password", "")
        try:
            user = authenticate(username=username, password=password)
        except :
            return Response({"detail": "Invalid username/password."}, status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user=user)
        user_serializer = UserSerializer(user)
        return Response({
                "user": user_serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    
class UserRegistration(APIView):

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user and return JWT tokens upon successful registration.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username of User'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password of User'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='password of User'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='password of User'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='password of User'),
            },
        ),
        responses={
            201: 'User registered successfully',
            400: 'Invalid data provided'
        }
    )
    def post(self, request: Request):
        
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                    "user": user_serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Get user's cart items",
        operation_description="Retrieve all items in the authenticated user's shopping cart.",
        
        responses={
            200: CartItemSerializer(many=True),
            404: 'Cart not found'
        }
    )
    def get(self, request):
        
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Add a product to the user's cart",
        operation_description="Add a new product to the user's cart or update the quantity if it already exists.",
        
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_id', 'quantity'],
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the product', default=1)
            },
        ),
        responses={
            201: CartItemSerializer(),
            400: 'Invalid data'
        }
    )
    def post(self, request):
        
        user_cart = Cart.objects.get_or_create(user=request.user)[0]
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Update a cart item's quantity",
        operation_description="Update the quantity of an existing item in the user's cart.",
        
        request_body=CartItemSerializer,
        responses={
            200: CartItemSerializer(),
            404: 'Cart item not found',
            400: 'Invalid data'
        }
    )
    def put(self, request, pk):
        
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Delete a cart item",
        operation_description="Remove an item from the user's cart.",
        
        responses={
            204: 'Cart item successfully deleted',
            404: 'Cart item not found'
        }
    )
    def delete(self, request, pk):
        
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)