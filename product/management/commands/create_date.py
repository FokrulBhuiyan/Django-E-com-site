import requests
from django.core.management import BaseCommand
from product.models import Category,Product
from django.utils.text import slugify

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('creating date')
        response = requests.get('https://fakestoreapi.com/products').json()
        
        for product in response:
            category, _ = Category.objects.get_or_create(
                title = product['category'], 
                slug = slugify(product['category']),
                featured = True,
            )
            Product.objects.create(
                category=category,
                title = product['title'],
                slug = slugify(product['title']),
                price = product['price'],
                thumbnail = product['image'],
                desciption = product['description'],
            )
        print('inputting data is completed')