from email.headerregistry import Address
from rest_framework.viewsets import ModelViewSet
from .serializers import CardSerializer,AddressUserSerializer
from bigstore_api.infouser.models import Card,CardUser
from bigstore_api.infouser.models import Address as AddressUser
from rest_framework.response import Response
from rest_framework import status


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    lookup_field= 'pk'
    

    def list(self, request, *args, **kwargs):
        onlycarduser = CardUser.objects.filter(user_fk = request.user)
        info = [int(onlycarduser[x].card_fk.id) for x in range(len(onlycarduser))]
        listcard = Card.objects.filter(id__in=info)
        print(listcard ,onlycarduser)
        serializer = CardSerializer( listcard, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        print()
        try:
            create_card = Card.objects.create(name=request.data['name'],number=request.data['number'],date=request.data['date'],cvc=request.data['cvc'])
            create_card.save()
            new_card  = CardUser.objects.create(card_fk = Card.objects.last(),user_fk = request.user)
            new_card.save()
            return Response({"detail": "Card added successfully."}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "Error 400."}, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(ModelViewSet):
    serializer_class = AddressUserSerializer
    queryset = AddressUser.objects.all()
    lookup_field= 'pk'
    
    
    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)
    
    
    def create(self, request, *args, **kwargs):
        print(request.data['address2'])
        try:
            new_address = AddressUser.objects.create(id_user=request.user,
                                                     cep=request.data['cep'],
                                                     uf=request.data["uf"],
                                                     city=request.data['city'],
                                                     address1=request.data['address1'],
                                                     address2=request.data['address2']
                                                    )
            new_address.save()
            return Response({"detail": "Address added successfully."}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "HTTP_400_BAD_REQUEST."}, status=status.HTTP_400_BAD_REQUEST)
