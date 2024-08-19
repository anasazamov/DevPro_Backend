from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Product, Cart, CartItem
import base64

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Table', price=250.00, description='Wooden table')

    def test_get_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Check if pagination affects

    def test_get_single_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Table')

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'Chair', 'price': 75.00, 'description': 'Plastic chair'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        data = {'name': 'Updated Table', 'price': 300.00, 'description': 'Updated description'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class UserRegistrationAndTokenTest(APITestCase):
    def test_user_registration(self):
        url = reverse('user-registration')
        data = {'username': 'newuser', 'password': 'newpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('user' in response.data and 'refresh' in response.data)

    def test_get_token(self):
        
        username = 'testuser'
        password = 'testpassword123'
        user = User.objects.create_user(username=username, password=password)
        self.client.force_authenticate(user=user)  

        response = self.client.post(reverse('get-token'), data={"username": username, "password": password})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)  

        # Qo'shimcha tekshiruvlar
        self.assertTrue('refresh' in response.data)  
        self.assertEqual(response.data['user']['username'], username)  

class CartAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cartuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Desk', price=300.00, description='Office desk')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

    def test_add_product_to_cart(self):
        url = reverse('cart-detail')
        data = {'product_id': self.product.id, 'quantity': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cart_item(self):
        url = reverse('cart-item', kwargs={'pk': self.cart_item.id})
        data = {'quantity': 2}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart_item(self):
        url = reverse('cart-item', kwargs={'pk': self.cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
