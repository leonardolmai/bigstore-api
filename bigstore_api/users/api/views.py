from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bigstore_api.users.api.permissions import IsBigstore, IsCompany, IsCustomer, IsEmployee, IsEmployeeBigstore
from bigstore_api.users.models import Company, UserCompany

from .serializers import CompanySerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def type(self, request):
        if IsBigstore().has_permission(request, self):
            userType = "Bigstore"
        elif IsEmployeeBigstore().has_permission(request, self):
            userType = "Employee (Bigstore)"
        elif IsEmployee().has_permission(request, self):
            userType = "Employee"
        elif IsCustomer().has_permission(request, self):
            userType = "Customer"
        elif IsCompany().has_permission(request, self):
            userType = "Company"
        else:
            userType = "Normal User"

        return Response(status=status.HTTP_200_OK, data={"type": userType})


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(owner=self.request.user.id)

    @action(detail=True, methods=["GET", "POST", "DELETE"])
    def employees(self, request, pk):
        company = get_object_or_404(Company, pk=pk)

        if request.user != company.owner:
            return Response(
                {"detail": "You are not authorized to access this resource."}, status=status.HTTP_403_FORBIDDEN
            )

        if request.method == "GET":
            user_companies = company.users.filter(is_employee=True)
            employees = [user_company.user for user_company in user_companies]
            serializer = UserSerializer(employees, many=True)
            return Response(serializer.data)

        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)

        if request.method == "POST":
            try:
                user_company = UserCompany.objects.get(user=user, company=company)
                if user_company.is_employee:
                    return Response({"detail": "Employee already exists."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user_company.is_employee = True
                    user_company.save()
                    return Response({"detail": "Employee added successfully."}, status=status.HTTP_201_CREATED)
            except UserCompany.DoesNotExist:
                UserCompany.objects.create(user=user, company=company, is_employee=True)
                return Response({"detail": "Employee added successfully."}, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            if user == company.owner:
                return Response(
                    {"detail": "The company owner cannot be removed as an employee."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            UserCompany.objects.filter(user=user, company=company, is_employee=True).update(is_employee=False)
            return Response({"detail": "Employee removed successfully."}, status=status.HTTP_204_NO_CONTENT)
