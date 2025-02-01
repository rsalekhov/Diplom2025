from celery import shared_task
from django.core.mail import send_mail
from .models import Order  # Импортируй модель Order

@shared_task
def send_order_confirmation(order_id):
    """
    Задача для отправки подтверждения заказа по email.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Подтверждение заказа №{order.id}"
        message = f"Ваш заказ №{order.id} успешно оформлен. Спасибо за покупку!"
        recipient_list = [order.customer_email]  # Предположим, что у заказа есть email клиента
        send_mail(subject, message, 'from@example.com', recipient_list)
    except Order.DoesNotExist:
        # Обработка случая, если заказ не найден
        print(f"Заказ с ID {order_id} не найден.")