from rest_framework import serializers

from bigstore_api.addresses.models import Address
from bigstore_api.users.api.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Address
        fields = ["id", "user", "postal_code", "uf", "city", "neighborhood", "street", "number", "complement"]
        read_only_fields = ["id", "user"]
