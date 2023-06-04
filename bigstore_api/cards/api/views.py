from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bigstore_api.cards.models import Card

from .serializers import CardSerializer


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    lookup_field = "pk"

    def list(self, request, *args, **kwargs):
        onlycarduser = Card.objects.filter(user=request.user)
        serializer = CardSerializer(onlycarduser, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            create_card = Card.objects.create(
                user=request.user,
                name=request.data["name"],
                number=request.data["number"],
                expiration_month=request.data["expiration_month"],
                expiration_year=request.data["expiration_year"],
                cvc=request.data["cvc"],
            )
            create_card.save()
            return Response({"detail": "HTTP 201 - Card Created!, successfully! 🧁."}, status=status.HTTP_201_CREATED)

        except IndexError:
            return Response({"detail": "Erro HTTP 400 - Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
