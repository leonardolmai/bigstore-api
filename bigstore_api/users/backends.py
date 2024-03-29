from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from bigstore_api.users.models import Company, UserCompany

User = get_user_model()


class UserActivationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user is None:
            raise AuthenticationFailed("Unable to log in with the provided credentials")

        company_cnpj = request.headers.get("x-company-cnpj")

        if company_cnpj:
            try:
                company = Company.objects.get(cnpj=company_cnpj)
                UserCompany.objects.get_or_create(user=user, company=company)
            except Company.DoesNotExist:
                raise serializers.ValidationError("Invalid company CNPJ")

        if user is not None and not user.is_active:
            user.is_active = True
            user.save()

            try:
                if user.company and not user.company.is_active:
                    user.company.is_active = True
                    user.company.save()
            except ObjectDoesNotExist:
                pass

        return user

    def user_can_authenticate(self, user):
        return True
