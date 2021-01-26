from rest_framework import serializers
from .models import *


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

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