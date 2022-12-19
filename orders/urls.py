from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
)

orders_router = DefaultRouter()

orders_router.register(r'cart', CartViewSet)
orders_router.register(r'cart-item', CartItemViewSet)
orders_router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(orders_router.urls))
]