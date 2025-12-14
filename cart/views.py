from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import CartItem
from .utils import get_cart


# Create your views here.


def cart_detail(request):
    cart = get_cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("products:product_detail", slug=product.slug)


def cart_remove(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart:cart_detail")



def cart_increment(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.quantity += 1
    item.save()
    return redirect("cart:cart_detail")

def cart_decrement(request, item_id):
    cart=get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart:cart_detail")
