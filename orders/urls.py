from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-canceled/", views.payment_canceled, name="payment_canceled"),
]