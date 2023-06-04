from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bigstore_api.addresses.models import Address

from .serializers import AddressSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = "pk"

    def list(self, request, *args, **kwargs):
        onlyaddressuser = Address.objects.filter(user=self.request.user)
        serializer = AddressSerializer(onlyaddressuser, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            new_address = Address.objects.create(
                user=request.user,
                postal_code=request.data["postal_code"],
                uf=request.data["uf"],
                neighborhood=request.data["neighborhood"],
                street=request.data["street"],
                number=request.data["number"],
                complement=request.data["complement"],
            )
            new_address.save()
            return Response({"detail": "Address Created, successfully! 🧁."}, status=status.HTTP_201_CREATED)

        except IndexError:
            return Response({"detail": "Erro HTTP 400 - Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
