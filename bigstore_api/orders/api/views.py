from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bigstore_api.addresses.models import Address
from bigstore_api.cards.models import Card
from bigstore_api.orders.api.serializers import OrderSerializer
from bigstore_api.orders.models import Order, OrderItem
from bigstore_api.products.models import Product
from bigstore_api.users.models import Company


class OrderViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        company_cnpj = self.request.headers.get("x-company-cnpj")
        try:
            company = Company.objects.get(cnpj=company_cnpj)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company CNPJ")
        return Order.objects.filter(company=company, user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            company_cnpj = self.request.headers.get("x-company-cnpj")
            user = self.request.user

            company = get_object_or_404(Company, cnpj=company_cnpj)

            payment_method = serializer.validated_data["payment_method"]
            card_id = request.data.get("card_id")
            address_id = request.data.get("address_id")
            products = request.data.get("products")

            if not card_id and serializer.validated_data["payment_method"] == "card":
                return Response(
                    {"detail": "Card ID is required for card payment."}, status=status.HTTP_400_BAD_REQUEST
                )

            if card_id:
                card = get_object_or_404(Card, id=card_id, user=user)

            address = get_object_or_404(Address, id=address_id, user=user)

            order_items = []
            total = 0.0

            for product_id, quantity in products.items():
                product = get_object_or_404(Product, id=product_id)

                if quantity <= 0:
                    return Response({"detail": "Invalid quantity for product."}, status=status.HTTP_400_BAD_REQUEST)

                if product.quantity >= quantity:
                    order_item = OrderItem(
                        order=None, product=product, name=product.name, quantity=quantity, price=product.price
                    )
                    order_items.append(order_item)

                    total += product.price * quantity
                    product.quantity -= quantity
                    product.save()
                else:
                    return Response({"detail": "Product out of stock."}, status=status.HTTP_400_BAD_REQUEST)

            if payment_method == "card" and card:
                payment_details = card.number
            elif payment_method == "pix":
                payment_details = "Pix payment"
            elif payment_method == "bank_slip":
                payment_details = "Bank Slip payment"

            delivery_address = f"{address.street}, {address.number}"
            if address.complement:
                delivery_address += f", {address.complement}"
            delivery_address += f", {address.neighborhood}, {address.city}, {address.uf}, {address.postal_code}"

            order = Order(
                user=user,
                company=company,
                payment_method=payment_method,
                payment_details=payment_details,
                delivery_address=delivery_address,
                total=total,
            )

            order.save()
            for order_item in order_items:
                order_item.order = order
                order_item.save()

            headers = self.get_success_headers(serializer.data)
            order_serializer = self.serializer_class(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
