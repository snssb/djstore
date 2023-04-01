from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory
from users.models import User


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')   # 'https://127.0.0.1:4000/'
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_lsit(self):
        path = reverse('products:index')
        response = self.client.get(path)

        # print(response.context_data['products'])
        # print(products[:3])
        # print(list(response.context_data['products']) == list(products[:3]))
        self._common_tests(response)
        self.assertEqual(list(response.context_data['products']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        # print(list(response.context_data['products']))
        # print(list(products.filter(category_id=category.id)))
        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['products']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')