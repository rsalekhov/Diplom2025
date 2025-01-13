from rest_framework import serializers
from .models import User, Product, Cart, CartItem, Contact, Order

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'company', 'position', 'type']


# Сериализатор для товара
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'supplier', 'characteristics', 'price', 'stock']

# Сериализатор для элемента корзины
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

# Сериализатор для корзины
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']

# Сериализатор для контактов
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address']

# Сериализатор для заказов
class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'contact', 'created_at', 'status']
