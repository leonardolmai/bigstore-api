from rest_framework import serializers

from bigstore_api.products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "quantity",
            "description",
            "is_approved",
            "created_by",
            "company",
            "category",
            "images",
        ]
        read_only_fields = ["id", "created_by", "company", "images"]
