from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product
from cart.models import Cart, CartItem
from cart.utils import get_cart
# Create your tests here.

class CartTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="TestCat")
        self.product = Product.objects.create(
            category=cat,
            name="Sample Product",
            price=200,
            stock=10,
        )

    def test_add_to_cart_creates_cartitem(self):
        url = reverse("cart:cart_add", args=[self.product.id])
        response = self.client.get(url)

        cart = get_cart(response.wsgi_request)
        item = CartItem.objects.get(cart=cart, product=self.product)

        self.assertEqual(item.quantity, 1)
        self.assertEqual(cart.total, 200)