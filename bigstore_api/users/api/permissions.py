import environ
from rest_framework.permissions import BasePermission

env = environ.Env()


class IsBigstore(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if hasattr(user, "company") and user.company is not None and user.company.cnpj == env("COMPANY_CNPJ"):
            return True
        return False


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if hasattr(user, "company") and user.company is not None:
            return True
        return False


class IsEmployeeBigstore(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_companies = user.companies.all()
        for user_company in user_companies:
            company = user_company.company
            if company.cnpj == env("COMPANY_CNPJ") and user_company.is_employee:
                return True
        return False


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        cnpj = request.headers.get("X-Company-CNPJ")
        user = request.user
        user_companies = user.companies.all()
        for user_company in user_companies:
            company = user_company.company
            if company.cnpj == cnpj and user_company.is_employee:
                return True
        return False


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        cnpj = request.headers.get("X-Company-CNPJ")
        user = request.user
        user_companies = user.companies.all()
        for user_company in user_companies:
            company = user_company.company
            if company.cnpj == cnpj and not user_company.is_employee:
                return True
        return False
