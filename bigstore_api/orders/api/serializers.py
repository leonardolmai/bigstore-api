from rest_framework import serializers

from bigstore_api.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "name", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "company",
            "status",
            "created_at",
            "payment_method",
            "payment_details",
            "delivery_address",
            "total",
            "order_items",
        ]
        read_only_fields = ["id", "user", "company", "total", "payment_details", "delivery_address", "order_items"]
