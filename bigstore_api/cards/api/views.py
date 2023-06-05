from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bigstore_api.cards.api.serializers import CardSerializer
from bigstore_api.cards.models import Card


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save(user=request.user)
        except IntegrityError:
            raise serializers.ValidationError("Card with this number already exists in your account.")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
