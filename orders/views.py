from rest_framework import viewsets
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)
from .models import (
    Cart,
    CartItem,
    Order,
)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
