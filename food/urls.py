from django.urls import path
from .views import *


urlpatterns = [
    path('', ItemAPI.as_view(), name='store'),
    path('cart/', OrderItemAPI.as_view(), name='cart'),
    path('add-to-cart/', AddToCartAPI.as_view(), name='add'),
    path('cart/<str:pk>/', OrderItemUpdateAPI.as_view(), name='update'),
    path('order/', OrderAPI.as_view()),
]
