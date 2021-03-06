from django.urls import path
from rest_framework.authtoken import views
from .views import *


urlpatterns = [
    path('', ItemAPI.as_view(), name='store'),
    path('filteritem/', FilterAPI),
    path('food-categories/', ClothSectionAPI.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('order-items/', OrderItemFilterAPI.as_view(), name='order-items'),
    path('users/', UserAPI.as_view(), name='users'),
    path('add-to-cart/', AddToCartAPI.as_view(), name='add'),
    path('cart/<str:pk>/', OrderItemUpdateAPI.as_view(), name='update'),
    path('order/', OrderAPI.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('address/', ShippingAdrressAPI.as_view()),
]
