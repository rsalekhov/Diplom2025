# products/management/commands/load_products.py
from django.core.management.base import BaseCommand
import yaml
from products.models import Shop, Category, Product, ProductInfo, Parameter  # Подключаем модели

class Command(BaseCommand):
    help = 'Load products from a YAML file'

    def handle(self, *args, **kwargs):
        # Указываем путь к вашему YAML файлу
        file_path = 'data/shop1.yaml'

        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

            # Пример загрузки данных из YAML в модели
            for shop_data in data.get('shops', []):  # Пример структуры YAML
                shop, created = Shop.objects.get_or_create(name=shop_data['name'])

                for category_data in shop_data.get('categories', []):
                    category, created = Category.objects.get_or_create(name=category_data['name'], shop=shop)

                    for product_data in category_data.get('products', []):
                        product, created = Product.objects.get_or_create(name=product_data['name'], category=category)

                        # Загрузка информации о продукте
                        for product_info_data in product_data.get('info', []):
                            ProductInfo.objects.get_or_create(product=product, info=product_info_data)

                        # Загрузка параметров продукта
                        for param_data in product_data.get('parameters', []):
                            Parameter.objects.get_or_create(product=product, parameter=param_data)

        self.stdout.write(self.style.SUCCESS('Data has been loaded successfully'))
