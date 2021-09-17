from django.db.models import fields
from api.user import models
from .models import Order
from rest_framework import serializers

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('user',)
        #TODO: add product and quantity