from django.test import TestCase
from django.urls import reverse
from your_app.models import Product
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Product, Cart, CartItem, Contact, Order
from .serializers import ProductSerializer, CartSerializer, ContactSerializer, OrderSerializer

# Главная страница
def index(request):
    return render(request, 'index.html')

# Список товаров с фильтрацией
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

# Корзина: просмотр
class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)

# Контакты: добавление
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

# Подтверждение заказа
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

# Просмотр заказов
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
