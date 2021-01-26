from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Item, OrderItem, Order
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_multiple_model.views import ObjectMultipleModelAPIView, FlatMultipleModelAPIView
from .serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, OrderItemUpdateSerializer
from django.contrib import messages
from django.utils import timezone


# class UserProfileAPI(generics.ListAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


class ItemAPI(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# class AddToCartAPI(APIView):
#     permission_classes = (AllowAny,)
#     # queryset = OrderItem.objects.all()
#     # serializer_class = OrderItemSerializer
#     def post(self, request, *args, **kwargs):
#         slug = request.data.get('slug', None)
#         user = request.data.get('user', None)
#         if slug is None:
#             return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
#         item = Item.objects.get(slug=slug)
#         order_item, created = OrderItem.objects.get_or_create(user=user, item=item)

#         order_qs = Order.objects.filter(user=user)
#         if order_qs.exists():
#             order = order_qs[0]
#             # check if the order item is in the order
#             if order.items.filter(item__slug=item.slug).exists():
#                 order_item.quantity += 1
#                 order_item.save()
#                 return Response(status=HTTP_200_OK)
#             else:
#                 order.items.add(order_item)
#                 return Response(status=HTTP_200_OK)
                
#         else:
#             ordered_date = timezone.now()
#             order = Order.objects.create(
#                 user=user)
#             order.items.add(order_item)
#             return Response(status=HTTP_200_OK)


class OrderItemAPI(ObjectMultipleModelAPIView):
    querylist = [
        {'queryset': Item.objects.all(), 'serializer_class': ItemSerializer},
        {'queryset': OrderItem.objects.all(), 'serializer_class': OrderItemSerializer},
        {'queryset': Order.objects.all(), 'serializer_class': OrderSerializer}

    ]


class OrderItemUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer


class OrderAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class AddToCartAPI(APIView):
    permission_classes = (AllowAny,)
    # queryset = OrderItem.objects.all()
    # serializer_class = OrderItemSerializer
    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({"message": "Invalid request"}, status=HTTP_400_BAD_REQUEST)
        item = Item.objects.get(slug=slug)
        order_item, created = OrderItem.objects.get_or_create(user=request.user, item=item)

        order_qs = Order.objects.filter(user=request.user)
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
                user=request.user)
            order.items.add(order_item)
            return Response(status=HTTP_200_OK)