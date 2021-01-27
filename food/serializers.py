from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=False)
    get_slug = serializers.ReadOnlyField()
    get_total = serializers.ReadOnlyField()
    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'get_slug', 'get_total', 'quantity')


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('quantity',)


class OrderSerializer(serializers.ModelSerializer):
    get_cart_total = serializers.ReadOnlyField()
    get_cart_items = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'