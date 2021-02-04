from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Item, OrderItem, Order, FoodSection
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_multiple_model.views import ObjectMultipleModelAPIView
from .serializers import RegisterSerializer, ItemSerializer, OrderItemSerializer, OrderSerializer, OrderItemUpdateSerializer, UserSerializer, FoodSectionSerializer
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class OrderItemFilterAPI(generics.ListAPIView):
    model = OrderItem
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user.id)


class UserAPI(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ItemAPI(ObjectMultipleModelAPIView):
    permission_classes = (AllowAny,)
    querylist = [
        {'queryset': Item.objects.all(), 'serializer_class': ItemSerializer},
        {'queryset': User.objects.all(), 'serializer_class': UserSerializer},
    ]

class FoodSectionAPI(generics.ListAPIView):
    model = FoodSection
    permission_classes = (AllowAny,)
    serializer_class = FoodSectionSerializer
    queryset = FoodSection.objects.all()


class ItemFilterAPI(generics.ListAPIView):
    model = Item
    serializer_class = ItemSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Item.objects.filter(food_section=4)


class OrderItemUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer


class OrderAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class AddToCartAPI(APIView):

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        id = request.data.get('id')
        user = User.objects.get(id=id)
        if slug is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        item = Item.objects.get(slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            user=user, item=item)

        order_qs = Order.objects.filter(user=user)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                return Response(status=HTTP_200_OK)
            else:
                order.items.add(order_item)
                return Response(status=HTTP_200_OK)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=user)
            order.items.add(order_item)
            return Response(status=HTTP_200_OK)
