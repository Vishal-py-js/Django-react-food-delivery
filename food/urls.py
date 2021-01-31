from django.urls import path
from rest_framework.authtoken import views
from .views import *


urlpatterns = [
    path('', ItemAPI.as_view(), name='store'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserAPI.as_view()),
    path('cart/', OrderItemAPI.as_view(), name='cart'),
    path('add-to-cart/', AddToCartAPI.as_view(), name='add'),
    path('cart/<str:pk>/', OrderItemUpdateAPI.as_view(), name='update'),
    path('order/', OrderAPI.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
]
