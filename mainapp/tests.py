from django.core.management import call_command
from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        test_category = ProductCategory.objects.create(name='Test')
        Product.objects.create(
            category=test_category,
            name='Product test 1'
        )
        Product.objects.create(
            category=test_category,
            name='Product test 2'
        )
        self.client = Client()

    def test_mainapp_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/product/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/product/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/product/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/product/prod/{product.id}/')
            self.assertEqual(response.status_code, 200)

