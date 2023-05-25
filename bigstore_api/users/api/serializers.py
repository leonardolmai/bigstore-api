from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers

from bigstore_api.users.models import Company, UserCompany

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    company_cnpj = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "cpf", "phone", "company_cnpj"]
        read_only_fields = ["id"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method == "POST":
            fields["email"].required = True
            fields["password"].required = True
            fields["company_cnpj"].required = True

        return fields

    def create(self, validated_data):
        company_cnpj = validated_data.pop("company_cnpj")

        try:
            company = Company.objects.get(cnpj=company_cnpj)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company CNPJ")

        try:
            user = User.objects.create_user(**validated_data)
            UserCompany.objects.create(user=user, company=company)

            return user
        except IntegrityError:
            raise serializers.ValidationError("Email address already exists.")


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "cnpj", "website", "owner", "is_active"]
        read_only_fields = ["id", "owner"]

    def create(self, validated_data):
        user = self.context.get("request").user

        try:
            company = Company.objects.create(owner=user, **validated_data)
            UserCompany.objects.create(user=user, company=company, is_employee=True)

            return company
        except IntegrityError:
            raise serializers.ValidationError("User already has a company.")


class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = ["id", "user_id", "company_id", "is_employee"]
        read_only_fields = ["id", "user_id", "company_id"]
