from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from bigstore_api.infouser.models import  Card, CardUser

User = get_user_model()


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id","name","number","date","cvc")


class CardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardUser
        fields = ("user_fk","card_fk")