from rest_framework import serializers

from .models import (
    Product,
    ProductCategory,
)


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'created_date',
            'pictures',
            'price',
            'discount',
            'category',
            'supplier',
        ]
