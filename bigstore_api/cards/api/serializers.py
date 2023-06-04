from rest_framework import serializers

from bigstore_api.cards.models import Card
from bigstore_api.users.api.serializers import UserSerializer


class CardSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Card
        fields = ("id", "user", "name", "number", "expiration_month", "expiration_year", "cvc")
