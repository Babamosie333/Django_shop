from django.test import TestCase
from products.models import Category, Product
from django.urls import reverse

# Create your tests here.

class ProductModelTests(TestCase):
    def test_product_str_returns_name(self):
        cat = Category.objects.create(name="TestCat")
        p = Product.objects.create(
            category=cat,
            name="Sample Product",
            price=100,
            stock=5,
        )
        self.assertEqual(str(p), "Sample Product")



class ProductListViewTests(TestCase):
    def test_product_list_page_loads(self):
        url = reverse("products:product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Products")