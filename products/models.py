from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Типы пользователей: Магазин и Покупатель
USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)

# Менеджер пользователя
class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Модель пользователя
class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')

    # Добавляем related_name для полей groups и user_permissions
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Уникальное имя для связи
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Уникальное имя для связи
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)

# Модель товара
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    supplier = models.CharField(max_length=255, verbose_name='Поставщик')
    characteristics = models.TextField(verbose_name='Характеристики')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество на складе')

    # Добавляем изображение товара
    image = ProcessedImageField(
        upload_to='products/',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 90},
        verbose_name='Изображение'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Модель корзины
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Корзина пользователя {self.user.email}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

# Модель элемента корзины
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

# Модель контактов
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

# Модель заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, verbose_name='Контакт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, default="Новый", verbose_name='Статус')

    def __str__(self):
        return f'Заказ {self.id} от {self.user.email}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
