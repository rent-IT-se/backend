from rest_framework import viewsets
from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
)
from .models import (
    Product,
    ProductCategory,
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_order=False)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()

