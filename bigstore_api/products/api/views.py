from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bigstore_api.products.api.serializers import ProductSerializer
from bigstore_api.products.models import Product, ProductImage
from bigstore_api.users.models import Company


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self, *args, **kwargs):
        company_cnpj = self.request.headers.get("x-company-cnpj")
        try:
            company = Company.objects.get(cnpj=company_cnpj)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company CNPJ")
        return self.queryset.filter(company=company)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company_cnpj = request.headers.get("x-company-cnpj")
        try:
            company = Company.objects.get(cnpj=company_cnpj)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company CNPJ")

        product = serializer.save(created_by=request.user, company=company, is_approved=False)

        images = request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST", "DELETE"], url_path=r"images(?:/(?P<image_pk>\d+))?")
    def images(self, request, pk, image_pk=None):
        if request.method == "POST":
            product = self.get_object()
            images = request.FILES.getlist("images")

            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            if image_pk is None:
                return Response({"detail": "Image ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

            product_image = get_object_or_404(ProductImage, pk=image_pk)
            product_image.delete()

            return Response({"detail": "Image removed successfully."}, status=status.HTTP_204_NO_CONTENT)
