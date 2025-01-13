from django.urls import path
from products.views import ProductListView, CartView, ContactCreateView, OrderCreateView, OrderListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView  # Для статической страницы

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  # Главная страница
    path('products/', ProductListView.as_view(), name='product-list'),  # Список товаров
    path('cart/', CartView.as_view(), name='cart-view'),  # Корзина
    path('contacts/', ContactCreateView.as_view(), name='contact-create'),  # Добавление контакта
    path('orders/', OrderCreateView.as_view(), name='order-create'),  # Подтверждение заказа
    path('orders/list/', OrderListView.as_view(), name='order-list'),  # Список заказов
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
