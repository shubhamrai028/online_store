import pytest
from rest_framework import status
from rest_framework.test import APIClient
from store.models import Category, Product, Order
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_category():
    client = APIClient()
    response = client.post('/api/categories/', {'name': 'Electronics', 'description': 'Devices and gadgets'})
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_product():
    client = APIClient()
    category = Category.objects.create(name='Electronics', description='Devices and gadgets')
    response = client.post('/api/products/', {
        'name': 'Smartphone',
        'description': 'Latest model',
        'price': 699.99,
        'category': category.id,
        'stock': 10
    })
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_order_creation_insufficient_stock():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    category = Category.objects.create(name='Electronics', description='Devices and gadgets')
    product = Product.objects.create(name='Smartphone', description='Latest model', price=699.99, category=category, stock=0)
    response = client.post('/api/orders/', {'products': [product.id]})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
