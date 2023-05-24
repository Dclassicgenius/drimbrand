from django.test import TestCase
from django.urls import reverse
from .models import Category

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(category_name='Electronics', slug='electronics')

    def test_str_representation(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), category.category_name)

    def test_get_url(self):
        category = Category.objects.get(id=1)
        expected_url = reverse('products_by_category', args=[category.slug])
        self.assertEqual(category.get_url(), expected_url)

    def test_verbose_name_plural(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category._meta.verbose_name_plural, 'categories')

    def test_verbose_name(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category._meta.verbose_name, 'category')
