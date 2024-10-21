from rest_framework import viewsets
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import status

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ViewSet):
    def create(self, request):
        product_ids = request.data.get('products', [])
        total_amount = 0
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found: ' + str(product_id)}, status=status.HTTP_404_NOT_FOUND)

            if product.stock <= 0:
                return Response({'error': 'Insufficient stock for product: ' + product.name}, status=status.HTTP_400_BAD_REQUEST)
            total_amount += product.price
            product.stock -= 1  # Reduce stock
            product.save()

        order = Order.objects.create(user=request.user, total_amount=total_amount)
        order.products.set(product_ids)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
